import json
import boto3
client = boto3.client('iot-data')


def handler(event, context):

    body = event["body-json"]

	# 결과 반환
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }