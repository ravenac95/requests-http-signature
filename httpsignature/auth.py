import struct
import base64
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
from requests.auth import AuthBase
from paramiko.agent import Agent

class HttpSignatureAuth(AuthBase):
    def __init__(self):
        self._agent = None

    @property
    def agent(self):
        if not self._agent:
            self._agent = Agent()
        return self._agent

    def __call__(self, request):
        # get request
        request = self._create_signature(request)
        print request.headers
        return request

    def _create_signature(self, request):
        now = datetime.now()
        custom = request.headers['super'] = "dude"
        date = request.headers['Date'] = format_date_time(mktime(now.timetuple()))
        
        # Get key
        key = self.agent.get_keys()[1]
        # Sign headers
        ssh_data = key.sign_ssh_data(None, date + "\n" + custom)

        parts = []
        while ssh_data:
            length = struct.unpack('>I', ssh_data[:4])[0]
            bits = ssh_data[4:length+4]
            parts.append(bits)
            ssh_data = ssh_data[length+4:]
        raw_signature = parts[1]
        signature = base64.b64encode(raw_signature)
        
        print "WERAERAFA"
        print signature

        request.headers['Authorization'] = 'Signature keyId="somekey",algorithm="rsa-sha1",headers="date super" {0}'.format(signature)

        return request
