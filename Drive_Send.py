from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

filename = r"C:\Users\il184\Desktop\CSVfile_{0}.csv".format(yesterday)

def upload_func(f_name):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
    # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
    # Refresh them if expired
        gauth.Refresh()
    else:
    # Initialize the saved creds
        gauth.Authorize()
# Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)
    with open(f_name, "r") as file:
        file_drive = drive.CreateFile({'title':os.path.basename(file.name) })  
        file_drive.SetContentString(file.read()) 
        file_drive.Upload()
    with open("Log_file.txt", "a") as log_file:
        log_file.write("{} has been uploaded.\n".format(f_name))

upload_func(filename)
