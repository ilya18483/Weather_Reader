from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

filename = r"C:\Users\il184\Desktop\CSVfile_2019-05-30.csv"
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

with open(filename, "r") as file:
    file_drive = drive.CreateFile({'title':os.path.basename(file.name) })  
    file_drive.SetContentString(file.read()) 
    file_drive.Upload()

print("Files have been uploaded.")
