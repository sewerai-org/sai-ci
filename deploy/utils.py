import argparse
import boto3
import logging
import logging.handlers
import yaml
# Ignore ! in yaml. This is only looking for plugins
# and not trying to parse the entire document.
yaml.add_multi_constructor('!', lambda loader, suffix, node: None)

from environs import Env

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

env = Env()
key_id = env('SSM_KEY_ID')
aws_region = env('AWS_DEFAULT_REGION')


def load_serverless_yml():
    try:
        with open("serverless.yml", "r+") as f:
            yml = yaml.load(f, Loader=yaml.FullLoader)
            return yml
    except IOError:
        print("This command can only be run in a Serverless service directory")

def get_service_name():
    yml = load_serverless_yml()
    return yml['service']
    
def get_output_value(service_name, stage, key):
    client = boto3.client(
        'cloudformation',
        region_name=aws_region
        )

    stacks = client.describe_stacks(
        StackName=f'{service_name}-{stage}'
    )

    stack = stacks['Stacks'][0]
    status = stack['StackStatus']
    print(status)

    for outputs in stack['Outputs']:
        if key in outputs['OutputKey']:
            return outputs['OutputValue']


def put_ssm_parameter(args):
    logger.debug(args)
    client = boto3.client(
        'ssm',
        region_name=aws_region
    )

    stage = args.stage
    parameter = args.parameter
    service_name = args.name

    value = get_output_value(service_name, stage, parameter)
    parameter = parameter.upper()

    logger.debug(f'Setting {value} on /{stage}/{service_name}/{parameter}')

    response = client.put_parameter(
        Name=f'/{stage}/{service_name}/{parameter}',
        Value=f'{value}',
        Type='SecureString',
        KeyId=key_id,
        Overwrite=True
    )

    print(response)


if __name__ == "__main__":
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the "foo" command
    parser_ssm = subparsers.add_parser('ssm')
    parser_ssm.add_argument(
        'stage', type=str,
        help='The stage of the serverless app'
    )
    parser_ssm.add_argument(
        'parameter', type=str,
        help='The name of the variable in serverless.yml'
    )
    parser_ssm.add_argument(
        '-n', '--name', type=str,
        default=get_service_name(),
        help='The Service name in serverless app. Default is to look it up.'
    )
    parser_ssm.set_defaults(func=put_ssm_parameter)

    args = parser.parse_args()
    args.func(args)
