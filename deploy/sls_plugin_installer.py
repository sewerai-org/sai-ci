import subprocess
import yaml

# Ignore ! in yaml. This is only looking for plugins
# and not trying to parse the entire document.
yaml.add_multi_constructor('!', lambda loader, suffix, node: None)

plugins = None
with open("serverless.yml", "r+") as f:
    yml = yaml.load(f, Loader=yaml.Loader)
    plugins = yml['plugins']

for plugin in plugins:
    command = ['sls', 'plugin', 'install', '--name', plugin]
    subprocess.call(command)

print(f'Installed {plugins}')
