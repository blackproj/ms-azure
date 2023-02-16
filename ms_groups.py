import requests
from get_token.auth import generate_access_token


def get_groups():
	APP_ID = 'NEED_YOUR_TOKEN_HERE'
	SCOPES = ['Group.Read.All']
	GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
	access_token = generate_access_token(app_id = APP_ID, scopes = SCOPES)

	headers = {
		'Authorization': 'Bearer ' + access_token['access_token']
	}

	endpoint = GRAPH_ENDPOINT + '/groups'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		i = 0
		group_id = []
		data = response.json()
			
		print('Tenant groups found.')
		for group in data['value']:
			nth_int = str(i)
			print(nth_int + ") ***Name:", group['displayName'], "***Description:", group['description'], "***e-Mail:", group['mail'])
			group_id.append(group['id'])
			i += 1

		print()
		raw_group_number = input("Which group do you want select? Please, enter the group number: ")

		while not raw_group_number.isdigit() or int(raw_group_number) > len(group_id)-1:
			raw_group_number = input("Do you have inserted a wrong value. So, which group do you want select? Please, enter the group number: ")
			print()

		group_number = int(raw_group_number)
		return group_id[group_number]

	else:
		print(response.json())
		print(response)