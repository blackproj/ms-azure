import webbrowser
from datetime import datetime
import json
import os
import msal


GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

def generate_access_token(app_id, scopes):
    # Save Session Token as a token file
    access_token_cache = msal.SerializableTokenCache()

    # read the token file
    if os.path.exists('auth_api_token.json'):
        access_token_cache.deserialize(open("auth_api_token.json", "r").read())
        token_detail = json.load(open('auth_api_token.json',))
        token_detail_key = list(token_detail['AccessToken'].keys())[0]
        token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
        if datetime.now() > token_expiration:
            os.remove('auth_api_token.json')
            access_token_cache = msal.SerializableTokenCache()

    # assign a SerializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        # load the session
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        # authenticate your existing account on microsoft portal
        flow = client.initiate_device_flow(scopes=scopes)
        print()
        print("This script will ask access to your Microsoft account and may use one or more of the following permissions: \n[User.Read], [Files.Read.All], [Group.Read.All], [Reports.Read.All], [Mail.Read]\n\nPlease, note that this script will work ONLY if you use your Microsoft work or school account.")
        print('Now to grant access to your data, you will be redirected into the login page of your Microsoft account. \nPlease fill this user code into your browser to grant this application: ' + flow['user_code'])
        print()
        webbrowser.open('https://microsoft.com/devicelogin')
        token_response = client.acquire_token_by_device_flow(flow)

    with open('auth_api_token.json', 'w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response

if __name__ == '__main__':
    ...