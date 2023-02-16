import requests
from get_token.auth import generate_access_token


def get_logs():
	APP_ID = 'NEED_YOUR_TOKEN_HERE'
	SCOPES = ['Reports.Read.All']
	access_token = generate_access_token(app_id = APP_ID, scopes = SCOPES)

	headers = {
		'Authorization': 'Bearer ' + access_token['access_token']
	}

	print('Microsoft Teams user activity report found.')
	print()
	print('0) Full user activity report (User details)')
	print('1) Soft user activity report (User activity counts)')
	print('Note that soft user activity statistics are NOT a subset of full user activity statistics.')
	print()
	raw_log_number = input("Please, enter desidered choice: ")
	print()

	while not raw_log_number.isdigit() or int(raw_log_number) > 1:
		raw_log_number = input("Do you have inserted a wrong value. Please, enter a correct value: ")
		print()

	log_number = int(raw_log_number)
	if log_number == 0:
		# you chosen full user activity. Note that position 0 D7, position 1 D30, position 2 D90, position 3 D180
		logs_id = []
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityUserDetail(period='D7')")
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityUserDetail(period='D30')")
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityUserDetail(period='D90')")
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityUserDetail(period='D180')")

		print('You have requested full user activity report.')
		print('Select the length of time period to make the report in CSV format. You have several choices:')
		print('0) Last seven days - 7 days')
		print('1) Last month - 30 days')
		print('2) Last three months - 90 days')
		print('3) Last six months - 180 days')
		print()	
		raw_log_number = input("Please, enter desidered choice: ")

		while not raw_log_number.isdigit() or int(raw_log_number) > 3:
			raw_log_number = input("Do you have inserted a wrong value. So, which period do you want choose? Please, enter desidered value: ")
			print()

		log_number = int(raw_log_number)
		endpoint = logs_id[log_number]
		response = requests.get(endpoint, headers = headers)

		if response.ok:
			print()
			print('Downloading in progress..')
			print()
			with open("full_user_report.csv", "a") as f:
				print(response.text, file = f)
				print('Download of the file is now completed.')
		else:
			print(response.status)
			print(response)
	else:
		# you chosen soft user activity. Note that position 0 D7, position 1 D30, position 2 D90, position 3 D180
		logs_id = []
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityCounts(period='D7')")
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityCounts(period='D30')")
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityCounts(period='D90')")
		logs_id.append("https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityCounts(period='D180')")

		print('You have requested soft user activity report.')
		print('Select the length of time period to make the report in CSV format. You have several choices:')
		print('0) Last seven days - 7 days')
		print('1) Last month - 30 days')
		print('2) Last three months - 90 days')
		print('3) Last six months - 180 days')
		print()	
		raw_log_number = input("Please, enter desidered choice: ")

		while not raw_log_number.isdigit() or int(raw_log_number) > 3:
			raw_log_number = input("Do you have inserted a wrong value. So, which period do you want choose? Please, enter desidered value: ")
			print()

		log_number = int(raw_log_number)
		endpoint = logs_id[log_number]
		response = requests.get(endpoint, headers = headers)

		if response.ok:
			print()
			print('Downloading in progress..')
			print()
			with open("soft_user_report.csv", "a") as f:
				print(response.text, file = f)
				print('Download of the file is now completed.')
		else:
			print(response.status)
			print(response)