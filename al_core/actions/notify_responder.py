import json
import boto3

from st2common.runners.base_action import Action
from lib.util import json_serial


__all__ = [
    'SQSSendMessageActionRunner'
]


# pylint: disable=too-few-public-methods
class SQSSendMessageActionRunner(Action):
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
        region = self.config['aws_region']
        session_kwargs['aws_access_key_id'] = self.config['aws_access_key_id']
        session_kwargs['aws_secret_access_key'] = self.config['aws_secret_key']

        session = boto3.Session(**session_kwargs)
        client = session.client('sqs', region_name=region)

        if client is None:
            return False, 'boto3 client creation failed'

        response = client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(data))
        response = json.loads(json.dumps(response, default=json_serial))
        return True, response
