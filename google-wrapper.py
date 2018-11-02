#!/bin/python


from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

class DriveWrapper():
    def __init__(self,service):
        self.saved = False
        self.service = service
        self.folder = 'ToDo'
        self.pickleFile = 'tasks.pkl'
        self.folderMetadata = {
            'name': self.folder,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        self.fileMetadata = {
            'name': 'task.pkl'
        }


    def checkDrive(self):
        gFolder = self.service.files()\
                .list(q="name='ToDo' and mimeType='application/vnd.google-apps.folder'")\
                .execute()\
                .get('files', [])
        
        if not gFolder:   
            self.createFolder()
        else:
            self.folderMetadata['id'] = gFolder[0].get('id')
            print "The ToDo folder already exists on this GDrive"
    
    def createFolder(self):
        todoFolder = self.service.files().create(body=self.folderMetadata)
    
    def saveFile(self):
        media = MediaFileUpload('tasks.pkl')
        todoFile = self.service.files().create(body=self.fileMetadata,
                                               media_body=media,
                                               fields='id').execute()
        self.service.parents().insert(body=self.folderMetadata.get('id'),
                                               file=todoFile.get('id'),
                                               fields='id').execute()

        print todoFile.get('id')

    def syncList(self):
        pass

    def removeFolder(self):
        pass

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
    wrapper.checkDrive()
    wrapper.saveFile()
    
    #results = service.files().list(
    #    pageSize=10, fields="nextPageToken, files(id, name)").execute()
    #items = results.get('files', [])

if __name__ == '__main__':
    main()
