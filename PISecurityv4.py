import smtplib
import time
import os
import requests

from azure.storage.file import FileService
from azure.storage.file import ContentSettings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

from datetime import datetime, timedelta

from gpiozero import MotionSensor
from picamera import PiCamera

pir = MotionSensor(4)
camera = PiCamera()

photoList = []
timeList = []

def time_since_last_photo(last_photo_time):
    now = datetime.now()
    time_waiting = now - last_photo_time
    return time_waiting

def send_all_attachments(list_of_photos):
    # send an email with attachments for photo list
    send_mail(send_from= username,
              subject="There was a caller to the your Door",
              text=emailBody,
              send_to=["your_recipient"],
              files=list_of_photos)
    # iterate through list to delete photos
    for index in range(len(list_of_photos)):
        os.remove(photoList[index])
    # clear the contents of the photo list
    list_of_photos.clear()

def get_filename_datetime():
    # Use current date/time to get a jpg file name
    now = datetime.now()
    timeList[0] = now
    current = now.strftime("%d%m%y%H%M%S")
    return current + ".jpg"
        
def send_to_azure(fileService, fileName, filePath):
    fileService.create_file_from_path(
        'security',
        'securityPhotos',  # We want to create this blob in the 'securityPhotos' directory
        fileName,
        filePath,
        content_settings=ContentSettings(content_type='image/jpg'))
    print("File sent to Azure!")
    
def send_mail(send_from: str, subject: str, text: str, send_to: list, files= None):

    send_to= default_address if not send_to else send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['X-Priority'] = '1'
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
username = 'you@gmail.com'
password = 'PASSWORD'
default_address = [] 

# Login Details for Azure Storage
file_service = FileService(account_name='killianoneachtain', account_key='KEY')
file_service.create_share('security')
file_service.create_directory('security', 'securityPhotos')

cwd = os.getcwd()  # Get the current working directory (cwd)
path = cwd + "/securityPhotos"
# change file permissions
access_rights = 0o755

# create a photo directory if none exists
try:
    os.mkdir(path, access_rights)
except OSError:
    print ("Creation of the directory %s failed. \nFolder already exists!" % path)
else:
    print ("Successfully created the directory %s " % path)

path = cwd + "/securityPhotos/"

now = datetime.now()
timeList.append(now)

timeout = timedelta(days=0,hours=0,minutes=0,seconds=30)

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
emailBody = "Dear Customer, \nThere was a caller to your door at " + date_time + ". \nPlease find photo's attached for the recent motion.\n\n\n\n"

while True:
    #Get last entered datetime in timeList
    time_length = len(timeList)
    number_of_photos = len(photoList)
    if (time_length == 0):
        last_time = 0
    else:
        last_time = (len(timeList) - 1)
    
    #initialize timer to zero
    timer = timedelta(days=0,hours=0,minutes=0)
    
    while True:
        timer = time_since_last_photo(timeList[last_time])
        if(timer > timeout):
            #   gmail with attachments
            send_all_attachments(photoList)
            break
        elif(pir.motion_detected):
            break
        elif(number_of_photos == 0):
            break
        elif(number_of_photos == 15):
            send_all_attachments(photoList)
    
    # program waits here until there is a motion sensed
    pir.wait_for_motion()
    
    name = get_filename_datetime()
    photoPath = path + name
    photoList.append(photoPath)
    print("Motion DETECTED!")
    
    camera.capture(photoPath)
    
    #send files to Azure storage
    send_to_azure(file_service, name, photoPath)
 
    time.sleep(5)
