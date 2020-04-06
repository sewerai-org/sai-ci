import subprocess
from utils import (
    load_serverless_yml,
    get_plugin_verion
)


yml = load_serverless_yml()
plugins = yml.get('plugins', None)

for plugin in plugins:
    version = get_plugin_verion(plugin)
    command = ['sls', 'plugin', 'install', '--name', f'{plugin}@{version}']
    subprocess.call(command)

print(f'Installed {plugins}')
