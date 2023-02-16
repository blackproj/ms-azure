import requests
from get_token.auth import generate_access_token


def get_details():
	APP_ID = 'NEED_YOUR_TOKEN_HERE'
	SCOPES = ['User.Read']
	GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
	endpoint = GRAPH_ENDPOINT + '/me'
	access_token = generate_access_token(app_id = APP_ID, scopes = SCOPES)

	headers = {
		'Authorization': 'Bearer ' + access_token['access_token']
	}

	response = requests.get(endpoint, headers = headers)

	if response.ok:
		values = []
		data = response.json()

		values.append(data['givenName'])						# value 0
		values.append(data['displayName'])						# value 1
		values.append(data['userPrincipalName'])				# value 2
		values.append(data['id'])								# value 3

		return values

	else:
		print(response.json())
		print(response)