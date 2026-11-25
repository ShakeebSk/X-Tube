import boto3
from secret_keys import SecretKeys
import json

secret_keys = SecretKeys()
sqs_client = boto3.client("sqs", region_name=secret_keys.REGION_NAME)

ecs_client = boto3.client("ecs", region_name=secret_keys.REGION_NAME)


def poll_sqs():
    while True:
        response = sqs_client.receive_message(
            QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )

        for message in response.get("Messages", []):
            message_body = json.loads(message.get("Body"))  

            if (
                "Service" in message_body
                and "Event" in message_body
                and message_body.get("Event") == "s3:TestEvent"
            ):
                sqs_client.delete_message(
                    QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                    ReceiptHandle=message["ReceiptHandle"],
                )
                continue

            if "Records" in message_body:
                s3_record = message_body["Records"][0]["s3"]
                bucket_name = s3_record["bucket"]["name"]
                s3_key = s3_record["object"]["key"]

                response = ecs_client.run_task(
                    cluster="arn:aws:ecs:ap-south-1:662124509144:cluster/Shakeeb-TranscoderCluster",
                    launchType="FARGATE",
                    # taskDefinition="arn:aws:ecs:ap-south-1:662124509144:task-definition/video-transcoder:2",
                    taskDefinition = "arn:aws:ecs:ap-south-1:662124509144:task-definition/video-transcoder:1",
                    overrides={
                        "containerOverrides": [
                            {
                                "name": "video-transcoder",
                                "environment": [
                                    {"name": "S3_BUCKET", "value": bucket_name},
                                    {"name": "S3_KEY", "value": s3_key},
                                ],
                            }
                        ]
                    },
                    networkConfiguration={
                        "awsvpcConfiguration": {
                            "subnets": [
                                "subnet-00c22179350c01119",
                                "subnet-0c42ede7de275aff6",
                                "subnet-03c238828fb141848",
                            ],
                            "securityGroups": ["sg-0e1d416f10a940717"],
                            "assignPublicIp": "ENABLED",
                        }
                    },
                )

                print("ECS Task Started Successfully:")
                print(response)

                sqs_client.delete_message(
                    QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                    ReceiptHandle=message["ReceiptHandle"],
                )


poll_sqs()
"""  
poll sqs is

"""
