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

## Query Bedrock Quotas

Query cross-region inference quotas (TPM / RPM / TPD) for the Claude
model family using `query_bedrock_quotas.py`. The script reports both
the applied (account-level) value and the AWS default value, and
covers both regional (`us.*` / `eu.*`) and global (`global.*`)
inference profiles.

Models covered:
- Claude Opus 4.5 / 4.6 / 4.7
- Claude Sonnet 4.5 (V1 and V1 1M Context Length) / 4.6
- Claude Haiku 4.5

### Usage
```bash
python3 query_bedrock_quotas.py --region <aws_region>
python3 query_bedrock_quotas.py --region <aws_region> --format json
```

### Examples
```bash
python3 query_bedrock_quotas.py --region us-west-2
# Output (excerpt)
=== Claude Opus 4.6 V1 (us-west-2) ===
Quota                                                 Applied            Default
--------------------------------------------------------------------------------
Cross-region tokens per minute                      3,000,000          3,000,000
Cross-region requests per minute                       10,000             10,000
Model invocation max tokens per day             2,160,000,000      2,160,000,000
Global cross-region tokens per minute               3,000,000          3,000,000
Global cross-region requests per minute                10,000             10,000
Global cross-region tokens per day              4,320,000,000      4,320,000,000
```

Quotas that AWS has not published for a given model (e.g. Opus 4.7
currently only exposes TPM) are shown as `N/A` in the table and
`null` in JSON output.
