from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

filepath = r""

g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

with open(filepath, "r") as file:
    file_drive = drive.CreateFile({'title':os.path.basename(file.name) })  
    file_drive.SetContentString(file.read()) 
    file_drive.Upload()

print("Files have been uploaded.")
