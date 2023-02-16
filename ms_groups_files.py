import os
import sys
import requests
from get_token.auth import generate_access_token


APP_ID = 'NEED_YOUR_TOKEN_HERE'
SCOPES = ['Files.Read.All']
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
access_token = generate_access_token(app_id = APP_ID, scopes = SCOPES)

headers = {
	'Authorization': 'Bearer ' + access_token['access_token']
}

def get_stats(group_id):
	endpoint = GRAPH_ENDPOINT + '/groups/' + group_id + '/drive'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		data = response.json()
		try:
			print()
			print('Username:', data['owner']['group']['displayName'], 
				'(' + data['owner']['group']['email'] + ')')
			print('SharePoint ID resource:', data['id'])
			print('SharePoint root directory:', data['name'])
			print('SharePoint directory Web URL:', data['webUrl'])
			print('Last edit did from user:', data['lastModifiedBy']['user']['displayName'],
				'(' + data['lastModifiedBy']['user']['email'] + ')')
		except:
			print("ERROR, SOME DATA ARE MISSING. PLEASE TRY TO SELECT ANOTHER GROUP.")
			sys.exit(0)
	else:
		print(response.json())
		print(response)

def get_root(group_id):
	endpoint = GRAPH_ENDPOINT + '/groups/' + group_id + '/drive/root'
	end = GRAPH_ENDPOINT + '/groups/' + group_id + '/'
	response = requests.get(endpoint, headers = headers)

	if response.ok:
		tmp = []
		data = response.json()
		tmp.append(data)
		dict = {'value' : tmp}
		root_id = dict['value'][0]['id']
	else:
		print(response.json())
		print(response)

	return root_id

def get_root_list(group_id, bool, root_id, endpoint):
	print()
	while bool == True:
		# all_files_id contains id of files
		all_files_id = list_files(endpoint)							
		chosen_id = choose_file(all_files_id)
		bool_value = which_kind(chosen_id, group_id)

		# simple file - no folder here
		if(bool_value == True):								
			download_content(chosen_id, group_id)
			bool = False
		# file selected is a folder
		else:												
			bool_nested = is_dir_empty(chosen_id, group_id)	
			bool_nested = True
			endpoint_nested = GRAPH_ENDPOINT + '/groups/' + group_id + '/drive/items/' + chosen_id + '/children'
			get_root_list(group_id, bool_nested, root_id, endpoint_nested)

# list the root folder of groups cloud sharepoint
def list_files(endpoint):
	response = requests.get(endpoint, headers = headers)
	if response.ok:
		i = 0
		file_id = []
		data = response.json()
		for file in data['value']:
			nth_int = str(i)
			print(nth_int + ") ***NAME:", file['name'], "***SIZE:", file['size']/1000, "KB",
			"***LAST MODIFIED TIME:", file['fileSystemInfo']['lastModifiedDateTime'])
			file_id.append(file['id'])
			i += 1
	
	else:
		print(response.json())
		print(response)

	return file_id

def choose_file(list_id_files):
	print()
	raw_file_number = input("Which file do you want download? Please, enter the file number: ")
	while not raw_file_number.isdigit() or int(raw_file_number) > len(list_id_files)-1:
		raw_file_number = input("Do you have inserted a wrong value. So, which file do you want download? Please, enter the file number: ")
			
	file_number = int(raw_file_number)
	right_id_chosen_file = list_id_files[file_number]
	return right_id_chosen_file

def is_dir_empty(single_file_id, group_id):
		endpoint = GRAPH_ENDPOINT + '/groups/' + group_id + '/drive/items/' + single_file_id
		response = requests.get(endpoint, headers = headers)
		data = response.json()
		zero_item = data['folder']['childCount']
		if zero_item == 0:
			print()
			print("***EMPTY FOLDER***")
			print("Please, select another file or directory.")
			sys.exit(0)
		
		return False

def which_kind(single_file_id, group_id):
	endpoint = GRAPH_ENDPOINT + '/groups/' + group_id + '/drive/items/' + single_file_id + '?$select=file'
	response = requests.get(endpoint, headers = headers)
	tmp = []
	data = response.json()
	tmp.append(data)
	dict = {'value' : tmp}

	try:
		if "mimeType" in dict['value'][0]['file']:
			return True
	except:
		return False

def download_content(single_file_id, group_id):
	endpoint = GRAPH_ENDPOINT + f'/groups/' + group_id + '/drive/items/' + single_file_id
	pwd_dir = os.getcwd()
	save_location = os.path.join(pwd_dir, r'Group_downloads')
	if not os.path.exists(save_location):
		os.makedirs(save_location)

	## Step 1. get the file name
	response_file_info = requests.get(endpoint, 
		headers = headers, params={'select': 'name'} )
	file_name = response_file_info.json().get('name')

	print()
	print('Downloading in progress..')
	print()
	## Step 2. downloading OneDrive file
	response_file_content = requests.get(endpoint + '/content', headers = headers)
	with open(os.path.join(save_location, file_name), 'wb') as _f:
		_f.write(response_file_content.content)

	print('Download of the file is now completed.')
	sys.exit(0)