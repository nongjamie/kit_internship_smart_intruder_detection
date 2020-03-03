# Take the picture by clicking the button.
def capture_button(camera, button, time, datetime, bucket, os):
    print('... capture_button starts ...')
    while True:
        
        # Create image file
        camera.start_preview()
        button.wait_for_press()
        camera.stop_preview()
        pic_name = str(datetime.datetime.now())[:19:].replace(':', '-').replace(' ','_')
        pic_file_name = pic_name + '.jpg'
        pic_path_name = '../button-pic/' + pic_file_name
        camera.capture(pic_path_name)
        print('Take the picture: ' + pic_file_name)

        # Upload into firebase storage
        source_file_name = pic_path_name
        destination_blob_name = 'button-pic/' + pic_file_name
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
