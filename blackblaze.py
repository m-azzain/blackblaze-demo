import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from dotenv import load_dotenv
import os
import sys

load_dotenv()
config = {'bb_bucket': os.getenv("BUCKET"), 'bb_endpoint': os.getenv("ENDPOINT"), 'bb_key_id': os.getenv("KEY_ID"),
          'bb_app_key': os.getenv("APPLICATION_KEY")}


# Return a boto3 resource object for B2 service
def get_b2_resource():
    b2 = boto3.resource(service_name='s3',
                        endpoint_url=config['bb_endpoint'],     # Backblaze endpoint
                        aws_access_key_id=config['bb_key_id'],  # Backblaze keyID
                        aws_secret_access_key=config['bb_app_key'],  # Backblaze applicationKey
                        config=Config(
                            signature_version='s3v4',
                            retries={
                                'max_attempts': 3,
                                'mode': 'standard'
                            }
                    ))
    return b2


def blackblaze_file_read(f_name):
    try:
        b2 = get_b2_resource()
        obj = b2.Object(bucket_name=config['bb_bucket'], key=f_name)
        response = obj.get()
        return response['Body'].read()
    except Exception:
        print("while reading %s from blackblaze", f_name, sys.exc_info())
        raise
    return b''


def blackblaze_file_write(bin_value, f_name):
    try:
        b2 = get_b2_resource()
        try:
            # Check if the file already exist
            b2.Object(config['bb_bucket'], f_name).load()
        except ClientError as e:
            if e.response['Error']['Code'] == "404" or e.response['Error']['Code'] == 'NoSuchKey':
                # The object does not exist.
                response = b2.Bucket(config['bb_bucket']).put_object(Body=bin_value, Key=f_name)
            else:
                # Something else has gone wrong.
                raise
    except Exception:
        print("while writing %s to blackbaze", f_name, sys.exc_info())
        raise
