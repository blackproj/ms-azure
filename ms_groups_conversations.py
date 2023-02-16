import re
import requests
from get_token.auth import generate_access_token


APP_ID = 'NEED_YOUR_TOKEN_HERE'
SCOPES = ['Group.Read.All']
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
access_token = generate_access_token(app_id = APP_ID, scopes = SCOPES)

headers = {
	'Authorization': 'Bearer ' + access_token['access_token']
}

def get_channel(group_id, myinfo):
	endpoint = GRAPH_ENDPOINT + '/teams/' + group_id
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		i = 0
		channel_id = []
		tmp = []
		data = response.json()
		tmp.append(data)
		dict = {'value' : tmp}
		
		print()
		print('Group channels found.')
		for channel in dict['value']:
			nth_int = str(i)
			print(nth_int + ") ***Name: " + channel['displayName'] + " ***Description: " + channel['description'])
			channel_id.append(channel['internalId'])
			i += 1
		
		print()
		raw_channel_number = input("Which channel do you want select? Please, enter the number: ")
		while not raw_channel_number.isdigit() or int(raw_channel_number) > len(channel_id)-1:
			raw_channel_number = input("Do you have inserted a wrong value. So, which channel do you want select? Please, enter the conversation number: ")
			print()

		channel_number = int(raw_channel_number)
		id = channel_id[channel_number]
		get_conversation(endpoint, id, myinfo)
	
	else:
		print(response.json())
		print(response)

def get_conversation(endpoint, id, myinfo):
	endpoint = endpoint + '/channels/' + id + '/messages?$expand=replies'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		j = 1
		sender = ""
		data = response.json()
		
		print()
		print('Group Teams chats conversations found.')
		print('Please, note that both following chats and messages are listed from most recent one to older.')
		print()
		print()
		print()
		for message in data['value']:
			if message['replies']:
				for reply in message['replies']:
					if (reply['from']['user']['id'] == myinfo[3]):
						pass
					elif (reply['from']['user']['id'] != myinfo[3]):
						sender = reply['from']['user']['displayName']

				print("Chat", j, "details:")
				print()
				print("SENDER: " + sender)
				print("RECIPIENT: Me (" + myinfo[2] + ")")
				print()
				print("######## START #########")
				print()
				j += 1
				for reply in message['replies']:
					if (reply['from']['user']['id'] == myinfo[3]):
						nth_message = reply['body']['content']
						nth_message = re.sub(r'<.*?>', '', nth_message)
						print("Me: " + nth_message)
						print("[Time sent: " + reply['lastModifiedDateTime'] + "]")
						print()
					elif (reply['from']['user']['id'] != myinfo[3]):
						nth_message = reply['body']['content']
						nth_message = re.sub(r'<.*?>', '', nth_message)
						print(reply['from']['user']['displayName'] + " says: " + nth_message)
						print("[Time sent: " + reply['lastModifiedDateTime'] + "]")
						print()

		print("######### END ##########")

	else:
		print(response.json())
		print(response)