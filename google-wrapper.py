#!/bin/python


from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from datetime import datetime
import time
from os import path, mknod, utime, rename
import io

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

class DriveWrapper():
    def __init__(self,service):
        self.saved = False
        self.service = service
        self.pickleFile = 'tasks.pkl'
        self.fileName = 'tasks.pkl'
        self.checkFile()

    def checkFile(self):
        self.file = self.service.files().list(q="name='%s'" % self.fileName).execute()
        print self.file
        if not self.file.get('files'):
            self.createFile()
        else:
            self.id =  self.file['files'][0].get('id')
        self.syncFile()

    def createFile(self):
        media = MediaFileUpload('tasks.pkl')
        todoFile = self.service.files().create(body={
                                                    'name' : 'tasks.pkl'
                                                },
                                               media_body=media,
                                               fields='id').execute()
        self.id = todoFile.get('id')

    def lastRemoteUpdateEpoc(self):
         lastRemoteUpdate = str(datetime.strptime(self.service.files().get(fileId=self.id, fields='modifiedTime').execute().get('modifiedTime').replace('T','')[:-5], '%Y-%m-%d%H:%M:%S'))
         return int(time.mktime(time.strptime(lastRemoteUpdate, '%Y-%m-%d %H:%M:%S')))

    def lastLocalUpdateEpoc(self):
        try:
            return int(path.getctime(self.fileName))
        except OSError:
            return 0


    def syncFile(self):
        if self.lastRemoteUpdateEpoc() > self.lastLocalUpdateEpoc():
            print "Remote file is ahead of local cache, updating local cache..."
            rename(self.fileName,'.'+self.fileName+'.old')
            self.pull()
        else:
            self.push()

    def push(self):
        print "pushed"
        self.service.files().update(fileId=self.id, media_body=MediaFileUpload('tasks.pkl')).execute()
        utime(self.fileName,None)

    def pull(self):
        print "pulled"
        done = False
        downloader = MediaIoBaseDownload(io.FileIO('tasks.pkl','wb'), self.service.files().get_media(fileId=self.id))
        while done is False:
            status, done = downloader.next_chunk()
        self.service.files().update(fileId=self.id).execute()


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    
    wrapper = DriveWrapper(service)
    
    #results = service.files().list(
    #    pageSize=10, fields="nextPageToken, files(id, name)").execute()
    #items = results.get('files', [])

if __name__ == '__main__':
    main()
