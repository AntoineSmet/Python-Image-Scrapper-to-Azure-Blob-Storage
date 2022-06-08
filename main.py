import requests
from bs4 import BeautifulSoup as bs
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient

#Your Connexion String
MY_CONNECTION_STRING = "DefaultEndpointsProtocol************************"
#Your Container Name
MY_IMAGE_CONTAINER = "picture"
#Your local path
LOCAL_IMAGE_PATH = "..\Picture"
#change the url to the one you want to scrape
URL = 'WebSiteURL'

class AzureBlobStorage:
    def Scrapp(self):
        #create folder with the picture if it doesn't exist
        if not os.path.exists('.\Picture'):
            os.mkdir('.\Picture')
        os.chdir('.\Picture')
        #Change the number to begin where you want to start
        page_begin = 1
        #Change the number to the number of pages you want to scrape
        page_end = 230 + 1

        #If you want to scrape only one page, change the page_end to page_begin or delete the loop
        for page in range(page_begin, page_end):
            req = requests.get(URL + str(page))
            soup = bs(req.text, 'html.parser')
            images = soup.find_all('img')
            for images in images:
                name = images['src']
                alpha = images['src']
                link = 'WebSiteURL' + alpha
                print(link)
                #replace the name of the photo it's better :))
                with open(name.replace(' ', '-').replace('/', '').replace('"', "'").replace('.jpg','') + '.jpg','wb') as f:
                    im = requests.get(link)
                    f.write(im.content)
                    #check the name on the terminal
                    print('Writing: ', name)

    def __init__(self):
        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)

    def upload_all_images_in_folder(self):
        # Get all files with jpg extension and exclude directories
        all_file_names = [f for f in os.listdir(LOCAL_IMAGE_PATH)
                          if os.path.isfile(os.path.join(LOCAL_IMAGE_PATH, f)) and ".jpg" in f]
        # Upload each file
        for file_name in all_file_names:
            self.upload_image(file_name)

    def upload_image(self, file_name):
        # Create blob with same name as local file name
        blob_client = self.blob_service_client.get_blob_client(container=MY_IMAGE_CONTAINER,
                                                               blob=file_name)
        # Get full path to the file
        upload_file_path = os.path.join(LOCAL_IMAGE_PATH, file_name)
        # Create blob on storage
        # Overwrite if it already exists!
        image_content_setting = ContentSettings(content_type='image/jpeg')
        print(f"uploading file - {file_name}")
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=image_content_setting)

    def upload_all_images_in_folder(self):
        # Get all files with jpg extension and exclude directories
        all_file_names = [f for f in os.listdir(LOCAL_IMAGE_PATH)
                          if os.path.isfile(os.path.join(LOCAL_IMAGE_PATH, f)) and ".jpg" in f]
        # Upload each file
        for file_name in all_file_names:
            self.upload_image(file_name)

# Initialize class and upload files
azure_blob_file_uploader = AzureBlobStorage()
azure_blob_file_uploader.Scrapp()
azure_blob_file_uploader.upload_all_images_in_folder()