from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    
    file_overwrite = False
    default_acl = 'public'
    bucket_name="meta-morph"