import boto3
import os
import json

bucketName = os.environ.get('BUCKET')


def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        if method == 'GET':
            if event['path'] == "/":
                s3_obj = boto3.client("s3")
                s3_clientObj = s3_obj.get_object(Bucket=bucketName, Key="users.json")
                s3_clientData = s3_clientObj['Body'].read().decode('utf-8')
                return {
                    'statusCode': 200,
                    'headers': {},
                    'body': json.loads(s3_clientData)
                }
        return {
            'statusCode': 400,
            'headers': {},
            'body': "We only accept GET /"
        }
    except Exception as e:
        body=json.dumps(e)
        return {
            'statusCode': 500,
            'headers': {},
            'body': body
        }
