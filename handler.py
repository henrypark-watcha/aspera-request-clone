import json, os, traceback, boto3
from urllib import response


def post_s3_event_to_ec2(event, context):

    print(f"event: {event}")

    key = event['Records'][0]['s3']['object']['key']

    ssm = boto3.client('ssm')
    command = "./test.sh"

    try:
        response = ssm.send_command(
            InstanceIds = [os.environ['INSTANCE_ID']],
            DocumentName = 'AWS-RunShellScript',
            Parameters = {
                'commands': [f'{command} "{key}"'],
                'workingDirectory': ['/home/ssm-user']
            }
        )

        command_id = response['Command']['CommandId']
        print(f"command_id: {command_id}")

        return {
            "statusCode": 200, 
            "body": "Request has been sent."
        }
    
    except Exception as e: 
        print(f"Error while ssm send command `touch {key}`, message: {e}")
        traceback.print_exc()
        raise e