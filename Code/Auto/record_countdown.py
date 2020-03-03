def record_countdown(camera, datetime, time, delay, duration, bucket, os):
    print('... record_countdown starts ...')
    while True:
        if delay <= 0:
            print('The countdown number should >= 1')
            print('Please try again ...')
            break
        else:
            
            # Create video file
            print('The record countdown feature will start in ...')
            countdown = delay
            while countdown >= 1:
                print(countdown)
                time.sleep(1)
                countdown -= 1
            video_name = str(datetime.datetime.now())[:19:].replace(':', '-').replace(' ','_')
            video_file_name = video_name + '.h264'
            video_path_name = '../countdown-video/' + video_file_name
            print('Start recording ...' + video_file_name)
            camera.start_recording(video_path_name)
            time.sleep(duration)
            print('Stop recording ...' + video_file_name)
            camera.stop_recording()
            
            # Upload into firebase storage
            source_file_name = video_path_name
            destination_blob_name = 'countdown-video/' + video_file_name
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            print('File {} uploaded to {}'.format(source_file_name, destination_blob_name))
            
            # Upload with overwrite the latest-video file
            source_file_name = pic_path_name
            destination_blob_name = 'latest-video.h264'
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            print('File {} uploaded by overwrite to {}'.format(source_file_name, destination_blob_name))
            
            # Delete uploaded file
            os.remove(video_path_name)
            
            time.sleep(1)