import requests
from httpsignature import HttpSignatureAuth

def test_request_main_index():
    """Test request on an http signature server"""
    # Basic usage will sign the Date header in the 
    # request using the first found ssh key
    http_signature_auth = HttpSignatureAuth() 
    # Requests response from the test server 
    # TODO will make a site that hosts the http signature server
    response = requests.get("http://127.0.0.1:8443", 
            auth=http_signature_auth)
    assert response.status_code == 200
