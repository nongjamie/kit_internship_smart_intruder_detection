def capture_countdown(camera, datetime, time, delay, bucket, os):
    print('... capture_countdown starts ...')
    while True:
        if delay <= 0:
            print('The countdown number should >= 1')
            print('Please try again ...')
            break
        else:
            
            # Create image file
            print('The capture countdown feature will start in ...')
            countdown = delay
            while countdown >= 1:
                print(countdown)
                time.sleep(1)
                countdown -= 1
            pic_name = str(datetime.datetime.now())[:19:].replace(':', '.')
            pic_file_name = pic_name + '.jpg'
            pic_path_name = '../countdown-pic/' + pic_file_name
            camera.capture(pic_path_name)
            print('Take the picture! ' + pic_file_name)
            
            # Upload into firebase storage
            source_file_name = pic_path_name
            destination_blob_name = 'countdown-pic/' + pic_file_name
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