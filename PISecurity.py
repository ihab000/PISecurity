import smtplib
import time
import os
import requests

from azure.storage.file import FileService
from azure.storage.file import ContentSettings
from datetime import datetime
from gpiozero import MotionSensor
from picamera import PiCamera

pir = MotionSensor(4)
camera = PiCamera()

def get_filename_datetime():
    # Use current date/time to get a jpg file name
    now = datetime.now()
    current = now.strftime("%d%m%y%H%M%S")
    return current + ".jpg"

def notify_by_email():
    gmail_user = 'killiansraspberrypi@gmail.com'
    gmail_password = 'MoW@x057xx'

    sent_from = gmail_user
    to = ["killiansraspberrypi@gmail.com", "killbags@gmail.com"]
    subject = 'OMG Super Important Message'
    body = "Hey, there was a motion sensed!"

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()   # optional
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from,
                        to,
                        email_text)
        server.quit()

        print ('Email sent!')
    # ...send emails
    except Exception as e:
        print (e)
        
def send_to_azure(fileService, fileName, filePath):
    fileService.create_file_from_path(
        'security',
        'securityPhotos',  # We want to create this blob in the 'securityPhotos' directory
        fileName,
        filePath,
        content_settings=ContentSettings(content_type='image/jpg'))
    os.remove(photoPath)
    print("File sent to Azure!")

# Login Details for Azure Storage
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
    notify_by_email()
    send_to_azure(file_service, name, photoPath)
    time.sleep(5)