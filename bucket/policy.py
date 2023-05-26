import json


def public_read_policy(bucket_name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            }
        ],
    }

    return json.dumps(policy)


def assign_public_read_policy(aws_s3_client, policy_function, bucket_name):
    policy = None
    response = None
    if policy_function == "public_read_policy":
        policy = public_read_policy(bucket_name)
        response = "public read policy assigned!"

    aws_s3_client.put_bucket_policy(
        Bucket=bucket_name, Policy=policy
    )

    print(response)
