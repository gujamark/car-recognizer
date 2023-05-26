import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import boto3
import uuid
from botocore.exceptions import ClientError

rekognition_client = boto3.client('rekognition')


def save_in_dynamodb(table, item):
    try:
        dynamodb_client = boto3.client("dynamodb")
        dynamodb_client.put_item(TableName=table,
                                 Item={"id": {"S": str(uuid.uuid4())}, "Analyzed Information": {"S": str(item)}})
    except ClientError as e:
        print(f"Client Error: {e}")


def recognize_car_from_url(image_url):
    try:
        data = {image_url: ""}
        req = Request("https://carnet.ai/recognize-url", data=urlencode(data).encode())
        response = urlopen(req).read().decode()
    except HTTPError as e:
        return False

    return json.loads(response)


def lambda_handler(event, context):
    for record in event.get("Records"):
        bucket = record.get("s3").get("bucket").get("name")
        key = record.get("s3").get("object").get("key")
        public_url = f"https://{bucket}.s3.amazonaws.com/{key}"
        print(public_url)
        print("Bucket", bucket)
        print("Key", key)
        carnet_result = recognize_car_from_url(public_url)
        print(carnet_result)
        if not carnet_result:
            rekognition_result = rekognition_client.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
            for label in rekognition_result["Labels"]:
                save_in_dynamodb("rekogintionAnalysesDB", label)
        else:
            save_in_dynamodb("carnetResponseDB", carnet_result)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
