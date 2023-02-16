import re
import requests
from get_token.auth import generate_access_token


# LIST 50 EMAILS WITH TOP SET TO 50 - MAXIMUM LIMIT IS SET TO 1000 - TO EDIT THIS PLEASE MODIFY endpoint
def get_emails():
	APP_ID = 'NEED_YOUR_TOKEN_HERE'
	SCOPES = ['Mail.Read']
	GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
	access_token = generate_access_token(app_id = APP_ID, scopes = SCOPES)

	headers = {
		'Authorization': 'Bearer ' + access_token['access_token'],
		'Prefer': 'outlook.body-content-type="text"'
	}

	endpoint = GRAPH_ENDPOINT + '/me/messages?$top=50&$select=sender, subject'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		i = 0
		email_id = []
		data = response.json()

		print('User e-mail found.')
		print('Note that e-mail are listed from most recent to older:')
		print()

		for email in data['value']:
			nth_int = str(i)
			print(nth_int + ") ***SUBJECT:", email['subject'], "***SENDER:" + ' (' + email['sender']
				['emailAddress']['address'] + ')')
			email_id.append(email['id'])
			i += 1
	else:
		print(response.json())
		print(response)

	print()
	raw_email_number = input("Which e-mail do you want read? Please, enter the e-mail number: ")
	isnumber = raw_email_number.isdigit()
	email_number = int(raw_email_number)
	while isnumber == True and email_number < 0 or email_number > len(email_id)-1:
		raw_email_number = input("Do you have inserted a wrong value. So, which e-mail do you want read? Please, enter the e-mail number: ")
		email_number = int(raw_email_number)

	id = email_id[email_number]
	endpoint = GRAPH_ENDPOINT + '/me/messages/' + id + '/?$select=sender, createdDateTime, subject, body, toRecipients'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		data = response.json()
		print()
		print()
		print("FROM:", data['sender']['emailAddress']['name'], '(' + data['sender']['emailAddress']['address'] + ')')
		print("SUBJECT:", data['subject'])
		print("TO:", data['toRecipients'][0]['emailAddress']['name'], '(' + data['toRecipients'][0]['emailAddress']['address'] + ')')
		print("SENT ON DATE:", data['createdDateTime'])
		print()
		print("TEXT:")
		print("######## START #########")
		nth_message = data['body']['content']
		nth_message = re.sub(r'<.*?>', '', nth_message)
		print(nth_message)
		print("######### END ##########")
	else:
		print(response.json())
		print(response)