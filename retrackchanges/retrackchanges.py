import base64
import io
import json

import docxlib

def lambda_handler(event, context):
    if event["requestContext"]["http"]["method"].upper() == "OPTIONS":
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('Hello from Lambda!')
        }
    elif event["requestContext"]["http"]["method"].upper() == "POST":
        with io.BytesIO(base64.b64decode(event["body"])) as inf, io.BytesIO() as outf:
            docxlib.remove_comment_timestamps(inf, outf)
            outf.seek(0)
            return {
                "statusCode": 200,
                "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "body": base64.b64encode(outf.getvalue()),
                "isBase64Encoded": True,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
            }
    
    raise ValueError(f"Unexpected: {event}")
