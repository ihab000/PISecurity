# Write your code here :-)
import time
import os

from azure.storage.file import FileService
from azure.storage.file import ContentSettings

from datetime import datetime

from gpiozero import MotionSensor
from picamera import PiCamera

def get_filename_datetime():
    # Use current date/time to get a jpg file name
    now = datetime.now()
    current = now.strftime("%d%m%y%H%M%S")
    return current + ".jpg"

pir = MotionSensor(4)
camera = PiCamera()


file_service = FileService(account_name='killianoneachtain', account_key='zqhzrvi/xUtwnmkY1RPM21+9UognHjjgu5SgDnSNP7VxGkSXA6YFDSwrmGIBwLJ7n92YPPhvHj/5b+P7s1ua/g==')

file_service.create_share('security')
file_service.create_directory('security', 'securityPhotos')


cwd = os.getcwd()  # Get the current working directory (cwd)
path = cwd + "/securityPhotos"
access_rights = 0o755

# create a photo directory if none exists
try:
    os.mkdir(path, access_rights)
except OSError:
    print ("Creation of the directory %s failed. \nFolder already exists!" % path)
else:
    print ("Successfully created the directory %s " % path)

while True:
    name = get_filename_datetime()
    #Get full path for writing
    path = cwd + "/securityPhotos/"
    photoPath = path + name
    pir.wait_for_motion()
    print("Motion DETECTED!")
    camera.capture(photoPath)
    file_service.create_file_from_path(
        'security',
        'securityPhotos',  # We want to create this blob in the 'securityPhotos' directory
        name,
        photoPath,
        content_settings=ContentSettings(content_type='image/jpg'))
    time.sleep(5)
    








