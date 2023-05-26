from myauto.images import parse_images
import boto3
from argparse import ArgumentParser
from auth import init_client
from bucket.crud import upload_folder_recursively
from bucket.policy import  assign_public_read_policy


def main():
    s3client = init_client()
    parser = ArgumentParser()

    parser.add_argument("--bucket-name", help="Bucket name where images will be uploaded", required=True)
    parser.add_argument("--save-directory", help="Folder name where images will be saved (local)",default="downloaded_images")
    args = parser.parse_args()

    if args.bucket_name and args.save_directory:
        parse_images(args.save_directory)
        upload_folder_recursively(s3client,args.bucket_name,args.save_directory)
        assign_public_read_policy(s3client,"public_read_policy",args.bucket_name)
main()