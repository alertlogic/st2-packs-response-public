import json
import requests
import boto3

from st2common.runners.base_action import Action
from lib.util import json_serial


__all__ = [
    'NotifyResponderActionRunner'
]


# pylint: disable=too-few-public-methods
class NotifyResponderActionRunner(Action):
    def run(self, data):
        if not isinstance(data, dict):
            return False

        queue_url = data.pop(
                'queue_url', 
                self.config.get('notifications_queue_url')
            )
        if not queue_url:
            return False

        session_kwargs = {}

        # endpoint_url = self.config.get('endpoint_url', "")
        region = self.config.get('aws_region', get_host_region())

        if 'aws_access_key_id' in self.config:
            session_kwargs['aws_access_key_id'] = self.config['aws_access_key_id']
            session_kwargs['aws_secret_access_key'] = self.config['aws_secret_key']

        session = boto3.Session(**session_kwargs)
        client = session.client('sqs', region_name=region)

        if client is None:
            return False, 'boto3 client creation failed'

        response = client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(data))
        response = json.loads(json.dumps(response, default=json_serial))
        return True, response


def get_host_region():
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html
    r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
    response_json = r.json()
    return response_json.get('region')
