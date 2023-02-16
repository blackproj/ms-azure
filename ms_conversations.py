import requests
import re
from get_token.auth import generate_access_token


APP_ID = 'NEED_YOUR_TOKEN_HERE'
SCOPES = ['Chat.Read']
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0' 
access_token = generate_access_token(app_id = APP_ID, scopes = SCOPES)

headers = {
	'Authorization': 'Bearer ' + access_token['access_token']
}

def get_list_conversations(myinfo):
	endpoint = GRAPH_ENDPOINT + '/me/chats?$expand=members'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		j = 0
		chat_id = []
		weburl_id = []
		recipients_name = []
		recipients_email = []
		data = response.json()

		print('User Teams chat conversations found.')
		print('Please, note that both following chats and messages are listed from most recent one to older.')
		print()

		for chat in data['value']:
			if (chat['chatType'] == "oneOnOne"):
				for j in range(2):
					if(chat['members'][j]['email'] != myinfo[2]):
						recipients_name.append(chat['members'][j]['displayName'])
						recipients_email.append(chat['members'][j]['email'])

			for id_no in data['value']:
				chat_id.append(id_no['id'])
				weburl_id.append(id_no['webUrl'])
				
		# removing duplicates from ID chats
		chat_id = list(dict.fromkeys(chat_id))

		for j in range(len(chat_id)):
			nth_int = str(j)
			print(nth_int + ") ***SENDER: " + recipients_name[j] + ' (' + recipients_email[j] +')')

		print()
		raw_chat_number = input("Which chat do you want read? Please, enter the chat number: ")

		while not raw_chat_number.isdigit() or int(raw_chat_number) > len(chat_id)-1:
			raw_chat_number = input("Do you have inserted a wrong value. So, which chat do you want read? Please, enter the chat number: ")
			print()

		chat_number = int(raw_chat_number)
		id = chat_id[chat_number]
		recipient_name = recipients_name[chat_number]
		recipient_email = recipients_email[chat_number]
		web_url = weburl_id[chat_number]
		
		get_conversation(id, recipient_name, recipient_email, web_url, myinfo)
	
	else:
		print(response.json())
		print(response)

def get_conversation(chat_id, sender, sender_mail, url, myinfo):
	endpoint = GRAPH_ENDPOINT + '/chats/' + chat_id + '/messages'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		data = response.json()

		print()
		print()
		print("SENDER: " + sender + " (" + sender_mail + ")")
		print("RECIPIENT: Me (" + myinfo[2] + ")")
		print()
		print("You can access directly to this chat at the following link: ")
		print(url)
		
		# print messages found on the chat selected minus last message because is empty
		print("######## START #########")
		for message in data['value'][:-1]:
			print()
			if (message['from']['user']['id'] == myinfo[3]):
				nth_message = message['body']['content']
				nth_message = re.sub(r'<.*?>', '', nth_message)
				print("Me: " + nth_message)
				print("[Time sent: " + message['lastModifiedDateTime'] + "]")
				print()
			elif (message['from']['user']['id'] != myinfo[3]):
				nth_message = message['body']['content']
				nth_message = re.sub(r'<.*?>', '', nth_message)
				print(message['from']['user']['displayName'] + " says: " + nth_message)
				print("[Time sent: " + message['lastModifiedDateTime'] + "]")
				print()
		
		print("######### END ##########")
	
	else:
		print(response.json())
		print(response)