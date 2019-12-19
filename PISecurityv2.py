import smtplib
import time
import os
import requests

#from idle_time import IdleMonitor

from azure.storage.file import FileService
from azure.storage.file import ContentSettings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

from datetime import datetime

from gpiozero import MotionSensor
from picamera import PiCamera

pir = MotionSensor(4)
camera = PiCamera()
#monitor = IdleMonitor.get_monitor()

def get_filename_datetime():
    # Use current date/time to get a jpg file name
    now = datetime.now()
    current = now.strftime("%d%m%y%H%M%S")
    return current + ".jpg"
        
def send_to_azure(fileService, fileName, filePath):
    fileService.create_file_from_path(
        'security',
        'securityPhotos',  # We want to create this blob in the 'securityPhotos' directory
        fileName,
        filePath,
        content_settings=ContentSettings(content_type='image/jpg'))
#    os.remove(photoPath)
    print("File sent to Azure!")
    
def send_mail(send_from: str, subject: str, text: str, send_to: list, files= None):

    send_to= default_address if not send_to else send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)  
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil: 
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype = ext)
            attachedfile.add_header(
                'content-disposition', 'attachment', filename=basename(f) )
        msg.attach(attachedfile)


    smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587) 
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
    print ('Email sent')

# Gmail login details
username = 'killiansraspberrypi@gmail.com'
password = 'password'
default_address = ['killiansraspberrypi@gmail.com'] 

# Login Details for Azure Storage
file_service = FileService(account_name='killianoneachtain', account_key='')
file_service.create_share('security')
file_service.create_directory('security', 'securityPhotos')

cwd = os.getcwd()  # Get the current working directory (cwd)
path = cwd + "/securityPhotos"
access_rights = 0o755

print ('I AM HERE!')

photoList = []
print (photoList)
motionCount = 0

# create a photo directory if none exists
try:
    os.mkdir(path, access_rights)
except OSError:
    print ("Creation of the directory %s failed. \nFolder already exists!" % path)
else:
    print ("Successfully created the directory %s " % path)

path = cwd + "/securityPhotos/"

now = datetime.now()
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
emailBody = "Dear Customer, \nThere was a caller to your door at " + date_time + ". \nPlease find photo's attached for the recent motion.\n\n\n\n"

while True:
    print ('I AM HERE 1!')
    #Get full path for writing
    print (photoList)
    # program waits here until there is a motion sensed
    
    pir.wait_for_motion()
    name = get_filename_datetime()
    photoPath = path + name
    photoList.append(photoPath)
    print("Motion DETECTED!")
    #now get time2 here
    # if time2 - time1 > 2 minutes
    camera.capture(photoPath)
    
#   gmail with attachments
    send_mail(send_from= username,
              subject="There was a caller to the your Door",
              text=emailBody,
              send_to=["20023634@mail.wit.ie"],
              files=photoList)
    #send files to Azure storage
    send_to_azure(file_service, name, photoPath)
    #here save the time
    then = datetime.now()
    time.sleep(5)
