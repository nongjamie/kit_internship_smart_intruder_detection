def capture_detect_intruder(pir, datetime, camera, time, bucket, os):
    print('... capture_detect_intruder starts ...')
    while True:
        
        # Create image file
        print('Wait for motion ...')
        pir.wait_for_motion()
        pic_name = str(datetime.datetime.now())[:19:].replace(':', '.')
        pic_file_name = pic_name + '.jpg'
        pic_path_name = '../intruder-pic/' + pic_file_name
        print('Motion detected! Take a picture! ' + pic_file_name)
        camera.capture(pic_path_name)
        
        # Upload into firebase storage
        source_file_name = pic_path_name
        destination_blob_name = 'intruder-pic/' + pic_file_name
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print('File {} uploaded to {}'.format(source_file_name, destination_blob_name))
        
        # Upload with overwrite the latest-picture file
        source_file_name = pic_path_name
        destination_blob_name = 'latest-picture.jpg'
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print('File {} uploaded by overwrite to {}'.format(source_file_name, destination_blob_name))
        
        # Delete uploaded file
        os.remove(pic_path_name)
        
        time.sleep(1)
