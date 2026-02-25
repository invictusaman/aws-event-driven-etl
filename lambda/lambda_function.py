import json

import boto3


def lambda_handler(event, context):
    # Extract file details from the S3 trigger event
    file_name = event["Records"][0]["s3"]["object"]["key"]
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]

    print("File Name:", file_name)
    print("Bucket Name:", bucket_name)

    # Initialize the Glue client
    glue = boto3.client("glue")

    # Start the Glue ETL job, passing file details as arguments
    # NOTE: "scriptNotebook" must match the exact script name saved in AWS Glue
    response = glue.start_job_run(
        JobName="scriptNotebook", Arguments={"--VAL1": file_name, "--VAL2": bucket_name}
    )

    print("Glue Job Started:", response["JobRunId"])

    return {
        "statusCode": 200,
        "body": json.dumps("Lambda triggered Glue successfully!"),
    }
