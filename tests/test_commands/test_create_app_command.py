import os
import shutil
import tempfile
from subprocess import call


def test_z_create_new_app():
    """
    Test creating a new app with createapp bootstrap command.
    """
    app_name = 'new_app'
    app_path = tempfile.mkdtemp()
    apps_py_bin = os.path.join(app_path, 'apps.py')

    env = os.environ.copy()

    args = ['arctic', 'createapp', app_name, app_path]
    retcode = call(args, env=env)

    assert retcode == 0
    assert os.path.exists(apps_py_bin)

    # cleanup test data
    shutil.rmtree(app_path)
