# S3 → Lambda → Glue Pipeline

An event-driven AWS data pipeline that automatically triggers an **AWS Glue ETL job** whenever a file is uploaded to an S3 bucket — orchestrated through **AWS Lambda** and monitored via **CloudWatch**.

---

## Architecture

```
S3 Bucket (source-bucket-takeo)
        │
        │  Upload Event
        ▼
AWS Lambda (lambda2glue)
        │
        │  Starts Glue Job with file_name + bucket_name
        ▼
AWS Glue — Script Editor (scriptNotebook)
        │
        │  Reads CSV from source S3
        ▼
S3 Bucket (dest-bucket-takeo)

        ↕  All logs monitored via CloudWatch
```

---

## Repository Structure

```
s3-lambda-glue-pipeline/
│
├── README.md                  ← You are here
│
├── docs/
│   ├── setup-guide.md         ← Full step-by-step setup instructions
│   └── architecture.md        ← Architecture overview and flow explanation
│
├── iam/
│   └── policy-reference.md    ← IAM role and permissions reference
│
├── lambda/
│   ├── lambda_function.py     ← Lambda handler code
│   └── README.md              ← Lambda setup notes
│
└── glue/
    ├── scriptNotebook.py      ← AWS Glue ETL script
    └── README.md              ← Glue setup notes
```

---

## Quick Start

Follow the steps in [`docs/setup-guide.md`](docs/setup-guide.md) in order:

1. Create IAM Role with required permissions
2. Create the S3 source bucket
3. Create and configure the Lambda function
4. Set up AWS Glue and attach the ETL script

---

## AWS Services Used

| Service           | Purpose                                 |
| ----------------- | --------------------------------------- |
| Amazon S3         | Source and destination storage          |
| AWS Lambda        | Event trigger and Glue job orchestrator |
| AWS Glue          | ETL processing of uploaded files        |
| Amazon CloudWatch | Logging and monitoring                  |
| AWS IAM           | Role-based access control               |

---

## Requirements

- An active AWS account
- Sufficient IAM permissions to create roles, Lambda functions, and Glue jobs
- Source and destination S3 buckets created in the same region
