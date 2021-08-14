import httplib2
import os

from googleapiclient.discovery import build, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from werkzeug.exceptions import Unauthorized

import logging
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'


class Authorize:
    def __init__(self, redirect):
        self.flow = InstalledAppFlow.from_client_secrets_file(get_api_creds_path(), SCOPES, redirect_uri=redirect)

    def start(self):
        return self.flow.authorization_url()[0]

    def complete(self, auth_code):
        self.flow.fetch_token(code=auth_code)
        with open('token.json', 'w') as token:
            token.write(self.flow.credentials.to_json())


def get_api_creds_path():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    return os.path.join(credential_dir, 'credentials.json')


def upload(filename, event, folder_id):
    if not os.path.exists('token.json'):
        raise Unauthorized("GDrive not authorized")

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    service = build('drive', 'v3', credentials=creds)

    media_body = MediaFileUpload(filename, mimetype='image/jpeg', resumable=True)
    body = {
      'name': os.path.basename(filename),
      'description': 'Event: %s' % event,
    }

    if folder_id:
        body['parents'] = [folder_id]

    try:
        upload = service.files().create(
        body=body,
        media_body=media_body).execute()
        logger.debug("Uploaded image to Drive (Id: %s)" % upload['id'])
    except:
        logger.exception("Could not upload image to Drive")
        

if __name__ == "__main__":
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    creds = Credentials.from_authorized_user_file('../token.json', SCOPES)

    if not creds or not creds.valid:
        print('Invalid credentials. Reauthorize Google API account access')

    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))