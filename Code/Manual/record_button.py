from picamera import PiCamera

# Take the picture by clicking the button.
def record_button(camera, button, datetime, time, bucket, os):
    print('... record_button starts ...')
    while True:
        
        # Create video file
        camera.start_preview()
        button.wait_for_press()
        video_name = str(datetime.datetime.now())[:19:].replace(':', '-').replace(' ','_')
        video_file_name = video_name + '.h264'
        video_path_name = '../button-video/' + video_file_name
        print('Start recording the video: ' + video_file_name)
        camera.start_recording(video_path_name)
        time.sleep(3)
        button.wait_for_press()
        camera.stop_preview()
        camera.stop_recording()
        print('Stop recording the video: ' + video_file_name)

        # Upload into firebase storage
        source_file_name = video_path_name
        destination_blob_name = 'button-video/' + video_file_name
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


