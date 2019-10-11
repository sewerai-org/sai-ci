import subprocess
import yaml

plugins = None
with open("serverless.yml", "r+") as f:
    yml = yaml.load(f, Loader=yaml.FullLoader)
    plugins = yml['plugins']

for plugin in plugins:
    command = ['sls', 'plugin', 'install', '--name', plugin]
    subprocess.call(command)

print(f'Installed {plugins}')
