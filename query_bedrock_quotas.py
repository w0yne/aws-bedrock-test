#!/usr/bin/env python3
"""Query AWS Bedrock service quotas for Claude cross-region inference models."""
import argparse
import json
import sys
import boto3
from botocore.exceptions import ClientError

MODELS = [
    "Opus 4.5",
    "Opus 4.6 V1",
    "Opus 4.7",
    "Sonnet 4.5 V1",
    "Sonnet 4.5 V1 1M Context Length",
    "Sonnet 4.6",
    "Haiku 4.5",
]

CATEGORIES = [
    ("regional", "tpm", "Cross-region tokens per minute",
     "Cross-region model inference tokens per minute for Anthropic Claude {model}"),
    ("regional", "rpm", "Cross-region requests per minute",
     "Cross-region model inference requests per minute for Anthropic Claude {model}"),
    ("regional", "tpd", "Model invocation max tokens per day",
     "Model invocation max tokens per day for Anthropic Claude {model} (doubled for cross-region calls)"),
    ("global",   "tpm", "Global cross-region tokens per minute",
     "Global cross-region model inference tokens per minute for Anthropic Claude {model}"),
    ("global",   "rpm", "Global cross-region requests per minute",
     "Global cross-region model inference requests per minute for Anthropic Claude {model}"),
    ("global",   "tpd", "Global cross-region tokens per day",
     "Global cross-region model inference tokens per day for Anthropic Claude {model}"),
]


def fetch_quotas(region):
    client = boto3.client("service-quotas", region_name=region)

    applied = {}
    for page in client.get_paginator("list_service_quotas").paginate(ServiceCode="bedrock"):
        for q in page["Quotas"]:
            applied[q["QuotaName"]] = q

    defaults = {}
    for page in client.get_paginator("list_aws_default_service_quotas").paginate(ServiceCode="bedrock"):
        for q in page["Quotas"]:
            defaults[q["QuotaName"]] = q

    return applied, defaults


def build_result(applied, defaults):
    result = {}
    for model in MODELS:
        model_entry = {"regional": {}, "global": {}}
        for scope, dim, _label, template in CATEGORIES:
            name = template.format(model=model)
            a = applied.get(name)
            d = defaults.get(name)
            if a is None and d is None:
                model_entry[scope][dim] = None
                continue
            model_entry[scope][dim] = {
                "quota_name": name,
                "quota_code": (a or d).get("QuotaCode"),
                "applied": a["Value"] if a else None,
                "default": d["Value"] if d else None,
            }
        result[f"Claude {model}"] = model_entry
    return result


def fmt(v):
    if v is None:
        return "N/A"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"


def print_table(region, result):
    for model_name, entry in result.items():
        print(f"\n=== {model_name} ({region}) ===")
        print(f"{'Quota':<42} {'Applied':>18} {'Default':>18}")
        print("-" * 80)
        for scope, dim, label, _template in CATEGORIES:
            q = entry[scope].get(dim)
            applied = fmt(q["applied"]) if q else "N/A"
            default = fmt(q["default"]) if q else "N/A"
            print(f"{label:<42} {applied:>18} {default:>18}")


def print_json(region, result):
    print(json.dumps({"region": region, "models": result}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Query Bedrock Claude cross-region inference quotas.")
    parser.add_argument("--region", required=True, help="AWS region (e.g., us-west-2)")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    try:
        applied, defaults = fetch_quotas(args.region)
    except ClientError as e:
        print(f"Error calling Service Quotas API: {e.response['Error']['Message']}", file=sys.stderr)
        sys.exit(1)

    result = build_result(applied, defaults)

    if args.format == "json":
        print_json(args.region, result)
    else:
        print_table(args.region, result)


if __name__ == "__main__":
    main()
