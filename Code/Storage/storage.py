from google.cloud import storage
import threading
import pyrebase
import time
import os

''' Global variable '''
bucket_name = 'fir-realtime-69681.appspot.com'

''' Setup '''
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GOOGLE_APPLICATION_CREDENTIALS.json'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

''' Create bucket '''
def create_bucket(bucket_name):
    global storage_client
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket_name))

''' Uploads a file to the bucket. '''
def upload_blob(source_file_name, destination_blob_name):
    global bucket
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print('File {} uploaded to {}'.format(source_file_name, destination_blob_name))
    
''' Download a file from the bucket'''
def download_blob(source_blob_name, destination_file_name):
    global bucket
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print('File {} downloaded to {}'.format(source_blob_name, destination_file_name))
    
    
''' List buckets & items '''
def list_buckets_and_items():
    global storage_client
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        print('Bucket name: ' + bucket.name)
        for item in bucket.list_blobs():
            print('\t' + item.name)

''' Get the list of items from folder '''
def list_items_in_bucket(folder_name):
    global bucket
    storage_list = []
    for item in bucket.list_blobs():
        if folder_name in item.name:
            item_name = item.name.replace(folder_name + '/', '')
            storage_list.append(item_name)
    return storage_list

''' Check & Upload into firebase storage for each folder'''
def upload_media(folder_name, delete_after_upload):
    
    # Initial variable
    local_list = []
    my_path = '../' + folder_name + '/'
    
    # Storage check
    storage_list = list_items_in_bucket(folder_name)
    
    # Local check
    for r, d, f in os.walk(my_path):
        for item in f:
            if item == 'README.txt':
                continue
            local_list.append(item)
    
    # Compare one by one, Upload the missing items
    if len(local_list) != 0:
        for local_item in local_list:
            if local_item in storage_list:
                continue
            else:
                source_file_name = my_path + local_item
                destination_blob_name = folder_name + '/' + local_item
                upload_blob(source_file_name, destination_blob_name)
    
    # Delete the local media which has uploaded to the storage server
    if delete_after_upload:
        for item in local_list:
            item_name = my_path + item
            os.remove(item_name)
    
    time.sleep(0.2)

''' Main method '''
list_of_folders = ['button-pic', 'button-video', 'countdown-pic', 'countdown-video', 'intruder-pic', 'intruder-video']
print('--- Start Check and Upload the remaining media ---')
for i in range(len(list_of_folders)):
    upload_media(list_of_folders[i], True)
time.sleep(0.5)
print('--- End Check and Upload the remaining media ---')
