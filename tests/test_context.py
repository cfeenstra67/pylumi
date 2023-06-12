import os
import subprocess

import psutil
import pylumi
import pytest
import shutil

from .conftest import resolve_value


def run_pgrep(pattern):
    proc = subprocess.Popen(
        ["pgrep", "-i", "pulumi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()

    assert not stderr

    pids = list(map(int, filter(None, stdout.decode().strip().split("\n"))))

    out = []

    for pid in pids:
        proc = psutil.Process(pid)
        # On linux child processes stick around as defunct after shutting down
        if proc.status() != psutil.STATUS_ZOMBIE:
            out.append(pid)

    return out


def test_list_plugins():
    with pylumi.Context() as ctx:
        plugins = ctx.list_plugins()
        assert plugins == []


@pytest.mark.parametrize("async_", [True, False])
def test_list_plugins_create_provider(async_):
    assert not run_pgrep("pulumi")

    with pylumi.Context() as ctx:
        provider = ctx.provider("aws", {"region": "us-east-2"})

        # Processes dont' get created until the configure() call.
        assert not run_pgrep("pulumi")

        provider.configure()

        proc_nums = run_pgrep("pulumi")
        assert len(proc_nums) == 1

        plugins = ctx.list_plugins()
        assert plugins == ["aws"]

    assert not run_pgrep("pulumi")


@pytest.mark.parametrize(
    "kind, name, version, config",
    [("resource", "aws", "2.1.0", {"region": "us-east-2"})],
)
def test_install_plugin(kind, name, version, config):
    plugin_kind = kind
    plugin_name = name
    plugin_version = version
    plugin_config = config

    plugins_home = os.path.abspath(os.path.expanduser("~/.pulumi/plugins"))

    plugin_dir = os.path.join(
        plugins_home, f"{plugin_kind}-{plugin_name}-v{plugin_version}"
    )

    def rmifexists():
        if os.path.isdir(plugin_dir):
            shutil.rmtree(plugin_dir)

    rmifexists()

    try:
        with pylumi.Context() as ctx:
            ctx.install_plugin(plugin_kind, plugin_name, plugin_version)

            assert os.path.isdir(plugin_dir)

            with ctx.provider(plugin_name, plugin_config, plugin_version) as provider:
                schema = provider.get_schema()
                assert schema["version"] == "v" + plugin_version
    finally:
        rmifexists()
