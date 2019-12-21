# PISecurity
Raspberry PI 4 based security IoT project

# Hardware Required

- Raspberry PI 4 with Internet/WiFi connection and Camera connection enabled
- PIR Module for Raspberry Pi
- Raspberry Pi Camera (B01)

# Software Required

- Node.js
- Python(3.*)
- Raspbian Buster / Buster Lite
- Blynk

# Mobile Applications

- Blynk with On/Off button project 
- Microsoft Azure Storage account

# Project Scope

This will activate / deactivate a python script, to take photo's from your Pi Camera. The Node.js script is run at startup of
the Pi and will be activated via Blynk. The index.js file will spawn the python script 'PISecurity.py'. This script communicates with the PIR module and Pi camera. 

When is a motion detected by the PIR, the camera will take a picture and store it on the SD card connected to Raspberry Pi. A timer starts after the photo is taken, and on timeout of thrity seconds, there is an email sent to a user with the attached photos. The file is also sent to Azure Storage and stored in this cloud 'File Sharing' facility.

If there is another motion in the thrity seconds timeout, another photo is taken and stored on the SD card. The file paths for the photo's are stored in a 'list'. As the size limit of a gmail message is 25Mb, a limit of 16 photos is allowed in the 'list'. The average file size of the jpg images is 1.2Mb. 

The python script checks the timer and on timeout or list exceeds 16, it will attach all the photos to an email and send it.  It will clear the photo list after sending the email, so that the next email will contain the new motions detected. 

To stop the process, deactivate (off) via the Blynk app. 

The node will still be running, and active. Only the python script will be stopped. To reactivate the security camera, ensure the button is 'on', using the Blynk app on your device.

- Killian O'Neachtain
