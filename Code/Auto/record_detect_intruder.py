def record_detect_intruder(pir, datetime, camera, time, duration, bucket, os):
    print('... record_detect_intruder starts ...')
    while True:
        
        # Create video file
        print('Wait for motion ...')
        pir.wait_for_motion()
        video_name = str(datetime.datetime.now())[:19:].replace(':', '-').replace(' ','_')
        video_file_name = video_name + '.h264'
        video_path_name = '../intruder-video/' + video_file_name
        print('Motion detected! Record the video! ' + video_file_name)
        print('Start recording ...' + video_file_name)
        camera.start_recording('../intruder-video/' + video_path_name)
        time.sleep(duration)
        camera.stop_recording()
        print('Stop recording ...' + video_file_name)

        # Upload into firebase storage
        source_file_name = video_path_name
        destination_blob_name = 'intruder-video/' + video_file_name
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
