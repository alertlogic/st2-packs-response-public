import json
import almdrlib

from st2common.runners.base_action import Action
from lib.util import json_serial

# pylint: disable=too-few-public-methods
class AlertLogicMDRActionRunner(Action):
    def run(self, service, action_name, credentials, params):
        session_kwargs = {}

        if credentials:
            session_kwargs['access_key_id'] = credentials.get('access_key_id')
            session_kwargs['secret_key'] = credentials.get('secret_key')
            session_kwargs['global_endpoint'] = credentials.get('global_endpoint')
            session_kwargs['aims_token'] = credentials.get('aims_token')
        else:
            session_kwargs['access_key_id'] = self.config['access_key_id']
            session_kwargs['secret_key'] = self.config['secret_key']
            session_kwargs['global_endpoint'] = self.config['global_endpoint']

        session = almdrlib.Session(**session_kwargs)
        client = session.client(service)

        if client is None:
            return False, 'almdrlib client creation failed'

        if params is not None:
            response = getattr(client, action_name)(**params)
        else:
            response = getattr(client, action_name)()

        response = json.loads(json.dumps(response.json(), default=json_serial))
        return True, response
