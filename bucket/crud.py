from pathlib import Path
import logging
from botocore.exceptions import ClientError


def bucket_exists(aws_s3_client, bucket_name) -> bool:
    try:
        response = aws_s3_client.head_bucket(Bucket=bucket_name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
    except ClientError:
        # print(e)
        return False


def upload_folder_recursively(aws_s3_client, bucket_name, filename):
    if not bucket_exists(aws_s3_client, bucket_name):
        raise ValueError("Bucket does not exists")

    root = Path(f'{filename}').expanduser().resolve()

    def __handle_directory(file_folder):
        if file_folder.is_file():
            upload_file(aws_s3_client, bucket_name, file_folder,
                        filename)
            return
        for each_path in file_folder.iterdir():
            if each_path.is_dir():
                __handle_directory(each_path)
            if each_path.is_file():
                upload_file(aws_s3_client, bucket_name, each_path,
                            str(each_path.relative_to(root)))

    __handle_directory(root)


def upload_file(aws_s3_client, bucket_name, file_path, filename):
    try:
        response = aws_s3_client.upload_file(file_path, bucket_name, filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True
