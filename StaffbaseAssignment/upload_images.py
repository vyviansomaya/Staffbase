import requests
import json
from setup_logger import logger

class ImageUploader():

    def __init__ (self,authKey,usersListUrl,folderPath,imageFormat):
        self.usersListUrl = usersListUrl
        self.authKey = authKey
        self.folderPath = folderPath
        self.imageFormat = imageFormat

    def get_usersList(self):
        usersAPI = self.usersListUrl
        headers = {'Authorization': 'Basic ' + self.authKey,
               'Content-Type': 'application/json; charset=UTF-8'}
        try:
            response = requests.get(usersAPI,headers=headers)
            response.raise_for_status
        except requests.exceptions.RequestException as e:
            logger.error("error in geeting usersList" + str(e))
            raise SystemExit(e)
    
        return json.loads(response.text)
    

    def post_picture(self,externalID):
        userURL = self.usersListUrl + '/'+ externalID
        headers = {'Authorization': 'Basic ' + self.authKey}
        files = {'avatar': ( externalID+'.'+self.imageFormat, open(self.folderPath+ '/'+externalID+'.'+self.imageFormat, 'rb'), 'image/'+self.imageFormat)}
        try:
            response = requests.put(userURL,headers=headers,files=files)
            response.raise_for_status
            logger.info("Image upload successful!")
        except requests.exceptions.RequestException as e:
            logger.error("error in uploading the image: " + str(e))
            raise SystemExit(e)

    def upload_images(self):
        folderPath = self.folderPath
        imageFormat = self.imageFormat 
    
        usersList = self.get_usersList()
        logger.info('uploading images to the users with externalID')
        logger.info('{} users found in the list'.format(len(usersList['data'])))
        for idx,user in enumerate(usersList['data']):
            externalID = user['externalID']
            logger.info('user : {}'.format(externalID))
            if open(folderPath+ '/'+externalID+'.'+imageFormat, 'rb'):
                self.post_picture(externalID)   
            else:
                logger.info('No image found for the externalId {}'.format(externalID))