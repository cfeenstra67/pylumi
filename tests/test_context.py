import subprocess

import pylumi


def run_pgrep(pattern):
    proc = subprocess.Popen(
        ['pgrep', '-i', 'pulumi'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()

    assert not stderr

    return list(map(int, filter(None, stdout.decode().strip().split('\n'))))


def test_list_plugins():
    with pylumi.Context() as ctx:
        plugins = ctx.list_plugins()
        assert plugins == []


def test_list_plugins_create_provider():
    
    assert not run_pgrep('pulumi')

    with pylumi.Context() as ctx:
        provider = ctx.provider('aws', {'region': 'us-east-2'})

        # Processes dont' get created until the configure() call.
        assert not run_pgrep('pulumi')

        provider.configure()

        proc_nums = run_pgrep('pulumi')
        assert len(proc_nums) == 1

        plugins = ctx.list_plugins()
        assert plugins == ['aws']

    assert not run_pgrep('pulumi')
