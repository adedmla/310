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
import datatier
import awsutil
import boto3     # AWS SDK


import requests  # calling web service
import jsons
from dotenv import load_dotenv

import uuid
import pathlib
import logging
import sys
import os 

from configparser import ConfigParser





def list_jobs(baseurl):
    """
        Function to list all the jobs on the web service
    """
    api = "/list"
    url = baseurl + api
    
    res = requests.get(url)
    
    body = res.json()
    
    if not body:
        print("No jobs found")
        return

    print("List of jobs:")
    print("====================================")
    for job in body['jobs']:
        print("Job ID: ", job['jobid'])
        print("Status: ", job['status'])
        


def status(baseurl):
    """
        Function to get the status of a job on the web service
    """
    user_input = input("Enter the job ID: ")
    api = "/status"
    url = baseurl + api + "/?jobid=" + user_input
    
    res = requests.get(url)
    body = res.json()
    
    if not body:
        print("No job found")
        return

    print("job ID: ", body['jobid'])
    print("Status: ", body['status'])
    return


def upload():
    """
        Function to upload a podcast to the web service
    """
    
    pass



def download(jobid):
    """
        Function to download a transcription from the web service
    """
    
    user_input = input("Enter the job ID: ")
    api = "/download"
    url = baseurl + api + "/?jobid=" + user_input
    
    res = requests.get(url)
    body = res.json()
    
    if not body:
        print("No job found")
        return

    print("job ID: ", body['jobid'])
    print("Status: ", body['status'])
    
    if body['status'] == "completed":
        print("Transcription is available for download")
        print("Downloading...")
        
        original_filename = body['original_filename']  
        original_filename = original_filename.split(".")[0] + ".txt"
        
        txtfilename = original_filename
        
        
        
        with open(txtfilename, "w", endcoding='utf-8') as f:
            f.write(transcript_text)

        
        print("Transcription downloaded to: ", txtfilename)
    else:
        print(f"Transcription not available for download. Current status: {body['status']}")
        print("Try again later")
        
        



def prompt():
    """
    Function to prompt user for input
        0 - Exit
        1 - Upload
        2 - Download
        3 - List
        4 - Status
    """
    try:
        print("Enter a commmand:  ")
        print("     0 - Exit")
        print("     1 - Upload")
        print("     2 - Download")
        print("     3 - List")
        print("     4 - Status")
        
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
    
    # initalizing config file
    config_file = 'podcastapp-config.ini'
    
    
    print("What config file to use for this session?")
    print("Press ENTER to use default (photoapp-config.ini),")
    print("otherwise enter name of config file>")
    s = input()

    if s == "":  # use default
      pass  # already set
    else:
      config_file = s
      
      
     #
    # does config file exist?
    #
    if not pathlib.Path(config_file).is_file():
      print("**ERROR: config file '", config_file, "' does not exist, exiting")
      sys.exit(0)
    
    # loading environment variables    
    load_dotenv()
    baseurl = os.getenv("BASE_URL")
    
    if baseurl is None:
        print("ERROR: BASE_URL not set")
        print("Exiting...")
        sys.exit(0)
    
    #
    # cleaning up the base URL
    #
    
    if len(baseurl) < 16:
        print("Invalid base URL")
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
            upload(baseurl)
        elif cmd == 2:
            download(baseurl)
        elif cmd == 3:
            list_jobs(baseurl)
        elif cmd == 4:
            status(baseurl)
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

   