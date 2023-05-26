# Description
This is a CLI script for automating aws services. This script automatically downloads images, uploads to bucket and creates a lambda function which is triggered when image is uploaded in S3 bucket. Then sends this image to Carnet API and AWS Rekognition to identify objects on the image

### Dependencies
- python3
- aiohttp
- boto3
- python-dotenv
- requests

Run `poetry install` to install required dependencies


### Prerequisities
- DynamoDB tables with following names (or you can change table names in serverless handler file):
  - carnetResponseDB
  - rekogintionAnalysesDB
- Fill out the `.env` file with the corresponding values

#### Serverless:
- install serverless with npm `npm install -g serverless`
- configure aws profile `aws configure`
- go in serverless directory and change `serverless.yml` file according to your needs
- run `serverless deploy`
- S3 Bucket for uploading images and Lambda Function for car recognisation will be created automatically

### Avaliable Flags

| Flag | Description | |
|-----|----|----|
| --bucket-name | Bucket name where images will be uploaded | Required |
| --save-directory | Directory name where images will be saved locally | Optional (Default: downloaded_images) |

## Examples
```
python main.py --bucket-name my-bucket --save-directory images
```
