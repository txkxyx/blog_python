import boto3
from web.service import utile

class AWS:
    ACCESS_KEY_ID = ''
    SECRET_ACCESS_KEY = ''
    REGION_NAME = ''

class S3(AWS):
    __BUCKET_NAME = ''
    
    def __init__(self):
        self.s3 = boto3.client('s3',
            aws_access_key_id = self.ACCESS_KEY_ID,
            aws_secret_access_key = self.SECRET_ACCESS_KEY,
            region_name = self.REGION_NAME)
        
    def put_obj(self, data):
        f_n = utile.rand_str(8) + '.png'
        self.s3.upload_fileobj(data, self.__BUCKET_NAME, f_n)
        return f_n
    
    def del_obj(self, key):
        if key != '':
            self.s3.delete_object(Bucket=self.__BUCKET_NAME, Key=key)