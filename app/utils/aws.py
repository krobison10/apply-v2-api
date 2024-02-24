import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv, find_dotenv
import os
from .json_error import JSONError

load_dotenv(find_dotenv())


class AWS:
    @staticmethod
    def s3_upload_file(bucket_name, file_name, file_content_bytes):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name="us-west-2",
        )

        try:
            s3_client.put_object(
                Bucket=bucket_name, Key=file_name, Body=file_content_bytes
            )

        except ClientError as e:
            JSONError.status_code = 500
            JSONError.throw_json_error("Failed to upload file to S3: " + str(e))

        return f"https://{bucket_name}.s3-us-west-2.amazonaws.com/{file_name}"

    @staticmethod
    def s3_delete_file(bucket_name, file_name):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name="us-west-2",
        )

        try:
            s3_client.delete_object(Bucket=bucket_name, Key=file_name)

        except ClientError as e:
            JSONError.status_code = 500
            JSONError.throw_json_error("Failed to delete file from S3: " + str(e))
