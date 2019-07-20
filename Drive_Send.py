from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

filename = r"\CSVfile_{0}.csv".format(yesterday)
folder_name = "csv_files"

def upload_func(f_name, folder_name):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)
    folders = drive.ListFile({'q': "title='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folders:
        if folder['title'] == folder_name:
            with open(f_name, "r") as file:
                file_drive = drive.CreateFile({'title':os.path.basename(file.name), 'parents': [{'id': folder['id']} ] })
                file_drive.SetContentString(file.read()) 
                file_drive.Upload()
    with open("Log_file.txt", "a") as log_file:
        log_file.write("{} has been uploaded.\n".format(f_name))

upload_func(filename, folder_name)