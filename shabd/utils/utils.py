from dropbox.dropbox_client import Dropbox
from storages.backends.dropbox import DropBoxStorage
from chat.settings import DROPBOX_OAUTH2_TOKEN
from django.core.files.base import ContentFile

dbx = Dropbox(DROPBOX_OAUTH2_TOKEN)

# Download file from dropbox account
def get_file_from_dropbox(file_url):
    if file_url:
        f, r = dbx.files_download(file_url)
        content_file = ContentFile(r.content, name=f.name)
    return content_file    