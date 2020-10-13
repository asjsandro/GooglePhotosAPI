import os
from Google import Create_Service
import pandas as pd
import requests

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 150)
pd.set_option('display.max_colwidth', 150)
pd.set_option('display.width', 150)
pd.set_option('expand_frame_repr', True)

CLIENT_SECRET_FILE = 'client_secret_GoogleCloudPlatform.json'
API_NAME = 'photoslibrary'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME,API_VERSION, SCOPES)

myAlbums = service.albums().list().execute()
myAlbums_list = myAlbums.get('albums')
dfAlbums = pd.DataFrame(myAlbums_list)

#print(dfAlbums)
#input('press any key to concinue!')
viagemparamanaus = dfAlbums[dfAlbums['title']== 'Viagem para Manaus']['id'].to_string(index=False).strip()

def download_file(url:str, destination_folder:str, file_name:str):
    response = requests.get(url)
    if response.status_code == 200:
        print('Download file {}'.format(file_name))
        with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)
            f.close()

media_files = service.mediaItems().search(body={'albumId':viagemparamanaus}).execute()['mediaItems']
print(media_files)
#input('press any key to continue')
destination_folder = r'Photos Backup'

for media_file in media_files:
    file_name = media_file['filename']
    download_url = media_file['baseUrl'] + '=d'
    download_file(download_url, destination_folder, file_name)