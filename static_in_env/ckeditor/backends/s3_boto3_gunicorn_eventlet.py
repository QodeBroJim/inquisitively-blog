"""
File backends with small tweaks to work with gunicorn + eventlet async
workers. These should eventually becom unecessary as the supporting libraries
continue to improve.
"""
import eventlet
from athumb.backends.s3boto3 import S3Boto3Storage, S3Boto3Storage_AllPublic

def eventlet_workaround(bytes_transmitted, bytes_remaining):
    """
    Stinks we have to do this, but calling this at intervals keeps gunicorn
    eventlet async workers from hanging and expiring.
    """
    eventlet.sleep(0)

class EventletS3Boto3Storage(S3Boto3Storage):
    """
    Modified standard S3Boto3Storage class to play nicely with large file
    uploads and eventlet gunicorn workers.
    """
    def __init__(self, *args, **kwargs):
        super(EventletS3Boto3Storage, self).__init__(*args, **kwargs)
        # Use the workaround as Boto3's set_contents_from_file() callback.
        self.s3_callback_during_upload = eventlet_workaround
        
class EventletS3Boto3Storage_AllPublic(S3Boto3Storage_AllPublic):
    """
    Modified standard S3Boto3Storage_AllPublic class to play nicely with large 
    file uploads and eventlet gunicorn workers.
    """
    def __init__(self, *args, **kwargs):
        super(EventletS3Boto3Storage_AllPublic, self).__init__(*args, **kwargs)
        # Use the workaround as Boto3's set_contents_from_file() callback.
        self.s3_callback_during_upload = eventlet_workaround