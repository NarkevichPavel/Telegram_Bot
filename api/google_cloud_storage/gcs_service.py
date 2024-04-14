from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


class GoogleCloudStorageService:
    auth = GoogleAuth()
    auth.LocalWebserverAuth()

    drive = GoogleDrive(auth)

    def create_file(self, file_name, path):
        try:
            file = self.drive.CreateFile({'title': file_name})

            file.SetContentFile(os.path.join(path, file_name))
            file.Upload()

            return file_name

        except Exception as e:
            return False

    def get_id_file(self, file_name):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

        for file in file_list:
            if file['title'] == file_name:
                return file.get('id')

    def get_file(self, file_name):
        file_id = self.get_id_file(file_name)

        file = self.drive.CreateFile({'id': file_id})
        file.GetContentFile(f'{file_name}')
