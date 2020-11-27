# Modified from https://github.com/asottile/setuptools-golang-examples
import argparse
import contextlib
import copy
import errno
import os
import platform
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
from distutils.ccompiler import CCompiler
from distutils.dist import Distribution
from types import TracebackType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type

from setuptools import Extension
from setuptools.command.build_ext import build_ext as _build_ext


def rmtree(path: str) -> None:
    """Newer golang uses readonly dirs & files for module cache."""
    def handle_remove_readonly(
            func: Callable[..., Any],
            path: str,
            exc: Tuple[Type[OSError], OSError, TracebackType],
    ) -> None:
        excvalue = exc[1]
        if (
                func in (os.rmdir, os.remove, os.unlink) and
                excvalue.errno == errno.EACCES
        ):
            for p in (path, os.path.dirname(path)):
                os.chmod(p, os.stat(p).st_mode | stat.S_IWUSR)
            func(path)
        else:
            raise
    shutil.rmtree(path, ignore_errors=False, onerror=handle_remove_readonly)


@contextlib.contextmanager
def _tmpdir() -> Generator[str, None, None]:
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        rmtree(tempdir)


def _get_cflags(
        compiler: CCompiler,
        macros: Sequence[Tuple[str, Optional[str]]],
) -> str:
    # https://github.com/python/typeshed/pull/3741
    args = [f'-I{p}' for p in compiler.include_dirs]  # type: ignore
    for macro_name, macro_value in macros:
        if macro_value is None:
            args.append(f'-D{macro_name}')
        else:
            args.append(f'-D{macro_name}={macro_value}')
    return ' '.join(args)


LFLAG_CLANG = '-Wl,-undefined,dynamic_lookup'
LFLAG_GCC = '-Wl,--unresolved-symbols=ignore-all'
LFLAGS = (LFLAG_CLANG, LFLAG_GCC)


def _get_ldflags() -> str:
    """Determine the correct link flags.  This attempts dummy compiles similar
    to how autotools does feature detection.
    """
    # windows gcc does not support linking with unresolved symbols
    if sys.platform == 'win32':  # pragma: no cover (windows)
        prefix = getattr(sys, 'real_prefix', sys.prefix)
        libs = os.path.join(prefix, 'libs')
        return '-L{} -lpython{}{}'.format(libs, *sys.version_info[:2])

    cc = subprocess.check_output(('go', 'env', 'CC')).decode('UTF-8').strip()

    with _tmpdir() as tmpdir:
        testf = os.path.join(tmpdir, 'test.c')
        with open(testf, 'w') as f:
            f.write('int f(int); int main(void) { return f(0); }\n')

        for lflag in LFLAGS:  # pragma: no cover (platform specific)
            try:
                subprocess.check_call((cc, testf, lflag), cwd=tmpdir)
                return lflag
            except subprocess.CalledProcessError:
                pass
        else:  # pragma: no cover (platform specific)
            # wellp, none of them worked, fall back to gcc and they'll get a
            # hopefully reasonable error message
            return LFLAG_GCC


def _check_call(cmd: Tuple[str, ...], cwd: str, env: Dict[str, str]) -> None:
    envparts = [f'{k}={shlex.quote(v)}' for k, v in sorted(tuple(env.items()))]
    print(
        '$ {}'.format(' '.join(envparts + [shlex.quote(p) for p in cmd])),
        file=sys.stderr,
    )
    subprocess.check_call(cmd, cwd=cwd, env=dict(os.environ, **env))


def _get_build_extension_methods(
        base: Type[_build_ext],
        root: str,
) -> Callable[[_build_ext, Extension], None]:

    def get_ext_filename(self, name: str) -> str:
        if name == 'libpylumigo':
            return 'libpylumigo.so'
        return base.get_ext_filename(self, name)

    def build_extension(self: _build_ext, ext: Extension) -> None:
        # If there are no .go files then the parent should handle this
        if not any(source.endswith('.go') for source in ext.sources):
            # the base class may mutate `self.compiler`
            compiler = copy.deepcopy(self.compiler)
            self.compiler, compiler = compiler, self.compiler

            ext_copy = copy.deepcopy(ext)
            build_lib = os.path.abspath(self.build_lib)
            ext_copy.include_dirs.append(build_lib)
            ext_copy.library_dirs.append('$ORIGIN')
            ext_copy.runtime_library_dirs.append('$ORIGIN')
            ext_copy.library_dirs.append(build_lib)
            ext_copy.runtime_library_dirs.append(build_lib)
            ext_copy.extra_link_args.append(f'-Wl,-rpath,{build_lib}')
            ext_copy.extra_link_args.append(f'-Wl,-rpath,$ORIGIN')

            ext_copy.libraries.append('pylumigo')

            try:
                return base.build_extension(self, ext_copy)
            finally:
                self.compiler, compiler = compiler, self.compiler

        if len(ext.sources) != 1:
            raise OSError(
                f'Error building extension `{ext.name}`: '
                f'sources must be a single file in the `main` package.\n'
                f'Recieved: {ext.sources!r}',
            )

        main_file, = ext.sources
        if not os.path.exists(main_file):
            raise OSError(
                f'Error building extension `{ext.name}`: '
                f'{main_file} does not exist',
            )
        main_dir = os.path.dirname(main_file)

        # Copy the package into a temporary GOPATH environment
        with _tmpdir() as tempdir:
            root_path = os.path.join(tempdir, 'src', root)
            # Make everything but the last directory (copytree interface)
            os.makedirs(os.path.dirname(root_path))
            shutil.copytree('.', root_path, symlinks=True)
            pkg_path = os.path.join(root_path, main_dir)

            env = {'GOPATH': tempdir}
            cmd_get = ('go', 'get', '-d')
            _check_call(cmd_get, cwd=pkg_path, env=env)

            env.update({
                'CGO_CFLAGS': _get_cflags(
                    self.compiler, ext.define_macros or (),
                ),
                'CGO_LDFLAGS': _get_ldflags(),
            })

            fname = ext.name + '.so'
            fpath = os.path.abspath(os.path.join(self.build_lib, fname))

            cmd_build = (
                'go', 'build', '-buildmode=c-shared',
                '-o', fpath,
            )
            _check_call(cmd_build, cwd=pkg_path, env=env)
            if platform.system() == 'Darwin':
                _check_call(['install_name_tool', '-id', '@loader_path/' + fname, fpath], cwd=pkg_path, env=env)

    return {
        'build_extension': build_extension,
        'get_ext_filename': get_ext_filename
    }


def _get_build_ext_cls(base: Type[_build_ext], root: str) -> Type[_build_ext]:
    return type('build_ext', (base,), _get_build_extension_methods(base, root))


def set_build_ext(
        dist: Distribution,
        attr: str,
        value: Dict[str, str],
) -> None:
    assert False
    root = value['root']
    # https://github.com/python/typeshed/pull/3742
    base = dist.cmdclass.get('build_ext', _build_ext)  # type: ignore
    dist.cmdclass['build_ext'] = _get_build_ext_cls(base, root)  # type: ignore
