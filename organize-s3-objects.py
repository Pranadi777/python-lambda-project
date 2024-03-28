#!/usr/bin/env python
# coding: utf-8

import boto3
from datetime import datetime

today = datetime.today()
todays_date = today.strftime("%Y%m%d")

def lambda_handler(event, context):

    #establish client
    s3_client = boto3.client('s3')

    #get the bucket and list it's objects
    bucket_name = "rpranadi-organize-s3-objects"
    list_objects_response = s3_client.list_objects_v2(Bucket=bucket_name)

    #focus in on the contents (i.e. the files of the bucket)
    get_contents = list_objects_response.get('Contents')

    #get the file names of the objects
    all_objs = []
    for item in get_contents:
        all_objs.append(item.get('Key'))

    #set the directory name
    directory_name = todays_date+"/"

    #create the directory if it is not there for 'today'
    if directory_name not in all_objs:
        s3_client.put_object(Bucket=bucket_name, Key=(directory_name))

    #For each object, copy it to the 'todays directory' if it has the same date creation (ignore directories that were cerated that day)
    for item in get_contents:
        #get each obj creation date
        obj_creation_date = item.get("LastModified").strftime("%Y%m%d")+"/"
        #get each obj name
        obj_name = item.get("Key")

        #checks if the object was created today, and that it is not a directory
        if obj_creation_date == directory_name and "/" not in obj_name:
            #if so, copy object to the directory of today
            s3_client.copy_object(Bucket=bucket_name, CopySource = bucket_name + "/" + obj_name, Key = directory_name+obj_name)
            #delete it from the main folder
            s3_client.delete_object(Bucket=bucket_name, Key=obj_name)



