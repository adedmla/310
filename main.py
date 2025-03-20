#
# Client-side python app for Vocalnk, working with a webservices,
# Which in turn uses AWS, S3, RDS, and Transcribe to implement 
# A simple transcribe tool for podcast transcription
#
#
# Authors
# <<<Omotayo Oludemi>>>
# <<<Adedamola Adejumobi>>>
#
#

import requests
import jsons


import uuid
import pathlib
import logging
import sys
import os 
import base64
import time

from configparser import ConfigParser




def upload():
    """
        Function to upload a podcast to the web service
    """
    pass
    
    



def download():
    """
        Function to download a transcription from the web service
    """
    pass



def prompt():
    """
    Function to prompt user for input
        0 - Exit
        1 - Upload
        2 - Download
    """
    
    print("Enter a commmand::  ")
    print("     0 - Exit")
    print("     1 - Upload")
    print("     2 - Download")
    
    
    try:
        print("Enter a commmand::  ")
        print("     0 - Exit")
        print("     1 - Upload")
        print("     2 - Download")
        
        command = int(input())
        return command
        
        
    except Exception as e:
        print("ERROR: ", e) 
        print("Invalid command")
        print("ERROR: ", e) 
        return -1
    
    


#########################################################################
## Main

try:
    print("** Welcome to VocalInk the one-stop shop for Transcribing Podcast**")
    print()
    
    # removing traceback
    sys.tracebacklimit = 0
    
    # Read configuration file
    config_file = "vocalink-config.ini"
    
    print("What Configuration file do you want to use?")
    print("Default: vocalink-config.ini, Press Enter to use default")
    print("Otherwise, enter the file name: ")   
     
    s = input()
    if s != "":
        pass
    else:
        config_file = s
        
    
    #
    # vailidating configuration file
    #
    
    if not pathlib.Path(config_file).is_file():
        print("Configuration file", config_file, "not found")
        print("Exiting...")
        sys.exit(0)
        
    #
    # Setup base URL to web service
    #
    
    configur = ConfigParser()
    configur.read(config_file)
    baseurl = configur.get("client", "webservice")
    
    
    #
    # cleaning up the base URL
    #
    
    if len(baseurl) < 16:
        print("Invalid base URL")
        print("Exiting...")
        sys.exit(0)
    
    if baseurl.startswith("https"):
        print("ERROR: Invalid base URL")
        print("ERROR: HTTPS not supported")
        print("Exiting...")
        sys.exit(0)

    if baseurl.endswith("/"):
        baseurl = baseurl[:-1]
    
    print("Base URL: ", baseurl) # debugging purposes
    
    #
    #
    # Main loop
    #
    
    cmd = prompt()
    while cmd != 0:
        
        if cmd == 1:
            upload()
        elif cmd == 2:
            download()
        else:
            print("Invalid command try a different command")    
        cmd = prompt()
        

    #
    # Finished
    #
    
    print()
    print("Thank you for using VocalInk hope to see you soon!!!")
    
except Exception as e:
    print("ERROR: ", e) 
    print("Exiting...")
    print("ERROR: ", e)

   