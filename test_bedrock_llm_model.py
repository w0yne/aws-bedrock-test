#!/usr/bin/env python3
import boto3
import argparse
from botocore.exceptions import ClientError

def test_bedrock_model(model_id, region=None):
    try:
        client = boto3.client('bedrock-runtime', region_name=region)
        
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "Who are you?"}]}],
            inferenceConfig={"maxTokens": 100, "temperature": 0.7}
        )
        
        print(f"Model: {model_id}")
        print(f"Response: {response['output']['message']['content'][0]['text']}")
        
    except ClientError as err:
        print(f"Error: {err.response['Error']['Message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test AWS Bedrock models')
    parser.add_argument('model_id', help='Bedrock model ID to test')
    parser.add_argument('--region', help='AWS region (defaults to CLI default)')
    
    args = parser.parse_args()
    test_bedrock_model(args.model_id, args.region)
