# aws-bedrock-test

```

## Setup

Install the latest version of boto3:
```bash
pip3 install --upgrade boto3
```

## Usage

Test AWS Bedrock models using the `test_bedrock_llm_model.py` script.

### Basic Usage
```bash
python3 test_bedrock_llm_model.py <model_id>
python3 test_bedrock_llm_model.py <model_id> --region <aws_region>
```

### Examples
```bash
python3 test_bedrock_llm_model.py us.anthropic.claude-3-7-sonnet-20250219-v1:0
# Output
Model: us.anthropic.claude-3-7-sonnet-20250219-v1:0
Response: I'm Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. I can have conversations, answer questions, assist with various tasks like writing or analysis, and generate different kinds of content based on your requests. I try to be thoughtful and thorough in my responses, while acknowledging my limitations. I don't have the ability to access the internet, run code, or take actions outside our conversation. How can I help you today?

python3 test_bedrock_llm_model.py us.anthropic.claude-sonnet-4-20250514-v1:0
# Output
Model: us.anthropic.claude-sonnet-4-20250514-v1:0
Response: I'm Claude, an AI assistant created by Anthropic. I'm here to help with a wide variety of tasks like answering questions, helping with analysis and research, creative writing, math and coding problems, or just having a conversation. Is there something specific I can help you with today?
```

### Requirements
- AWS credentials configured
- Access to Bedrock models
- Python 3 with boto3 >= 1.40.0
