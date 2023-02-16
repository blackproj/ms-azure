import ms_myself
import ms_files
import ms_logs
import ms_mail
import ms_conversations
import ms_groups
import ms_groups_files
import ms_groups_conversations
import ms_groups_logs


myinfo = ms_myself.get_details()
print()
print("Welcome user: " + myinfo[0], '(' + myinfo[2] + ')')
print("Through this script you will be able to access and download your e-mail, groups conversations, files and logs (report).")
print("First of all, you have to select the scope of queries.")
print()
print("0) User data")
print("1) Groups data")
print()
raw_choice = input("Please, enter desidered choice: ")

while not raw_choice.isdigit() or int(raw_choice) > 1:
    raw_choice = input("Do you have inserted a wrong value. Please, enter a correct value: ")
    print()

choice_number = int(raw_choice) 

if choice_number == 0:
    print()
    print("0) Access to your e-mails")
    print("1) Access to your Teams conversations")
    print("2) Access and download your files")
    print("3) Access and download your logs (report)")
    print()
    raw_choice = input("Do your choice: ")

    print()
    while not raw_choice.isdigit() or int(raw_choice) > 3:
        raw_choice = input("Do you have inserted a wrong value. Please, enter a correct value: ")
        print()

    choice_number = int(raw_choice) 

    if choice_number == 0:
        ms_mail.get_emails()
    elif choice_number == 1:
        ms_conversations.get_list_conversations(myinfo)
    elif choice_number == 2:
        ms_files.get_stats()
        bool_val = True
        root_id = ms_files.get_root()
        GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
        entry_point = GRAPH_ENDPOINT + '/me/drive/items/' + root_id + '/children'
        ms_files.get_root_list(bool_val, root_id, entry_point)
    elif choice_number == 3:
        ms_logs.get_logs()

else:
    print()
    print("0) Access to group Teams conversations")
    print("1) Access and download group files")
    print("2) Access and download group logs (reports)")
    print()
    raw_choice = input("Do your choice: ")
    print()
    while not raw_choice.isdigit() or int(raw_choice) > 2:
        raw_choice = input("Do you have inserted a wrong value. Please, enter a correct value: ")
        print()

    choice_number = int(raw_choice) 

    if choice_number == 0:
        group_id = ms_groups.get_groups()
        ms_groups_conversations.get_channel(group_id, myinfo)
    # choose the group to expand
    elif choice_number == 1:
        group_id = ms_groups.get_groups()                                   
        ms_groups_files.get_stats(group_id)
        bool_val = True
        root_id = ms_groups_files.get_root(group_id)
        GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
        entry_point = GRAPH_ENDPOINT + '/groups/' + group_id + '/drive/items/' + root_id + '/children'
        ms_groups_files.get_root_list(group_id, bool_val, root_id, entry_point)
    elif choice_number == 2:
        ms_groups_logs.get_logs()