import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


drive_folder_id = '1WXWclv-aHOZggDzjwvYOPgx81L_hCmzl'
save_folder = './tmp'
class dataDownlaod:
    def getAuth(self):
        gauth = GoogleAuth()
        # Try to load saved client credentials
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
        self.drive = GoogleDrive(gauth)

    def download_recursively(self, save_folder, drive_folder_id):
        # 保存先フォルダがなければ作成
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        max_results = 100
        query = "'{}' in parents and trashed=false".format(drive_folder_id)

        for file_list in self.drive.ListFile({'q': query, 'maxResults': max_results}):
            for file in file_list:
                print(file['title'])
                # mimeTypeでフォルダか判別
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    pass
                else:
                    base, ext = os.path.splitext(file['title'])
                    if  ext == ".csv":
                        print(file['title'])
                        file.GetContentFile(os.path.join(save_folder, file['title']))

d = dataDownlaod()
d.getAuth()
d.download_recursively(save_folder, drive_folder_id)

