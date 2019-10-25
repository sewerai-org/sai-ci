import subprocess
from utils import load_serverless_yml

yml = load_serverless_yml()
plugins = yml.get('plugins', None)

for plugin in plugins:
    command = ['sls', 'plugin', 'install', '--name', plugin]
    subprocess.call(command)

print(f'Installed {plugins}')
