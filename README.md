# AWS Event Driven ETL Pipeline with Glue and Lambda

> An event-driven AWS data pipeline that automatically triggers an AWS Glue ETL job whenever a file is uploaded to S3 — orchestrated through Lambda, with end-to-end visibility via CloudWatch.

---

## Overview

This project demonstrates how to connect **Amazon S3**, **AWS Lambda**, and **AWS Glue** into a fully automated, serverless ETL pipeline. When a CSV file lands in the source S3 bucket, a Lambda function is instantly triggered — it logs the event, then kicks off a Glue job that reads, processes, and writes the data to a destination bucket. No manual steps required after setup.

All executions are logged to **Amazon CloudWatch**, giving you full observability at every stage.

---

## Architecture

```
S3 Bucket (source-bucket-takeo)
        │
        │  PUT Event (file upload)
        ▼
AWS Lambda (lambda2glue)
        │  → Logs file name + bucket name to CloudWatch
        │  → Calls glue.start_job_run(scriptNotebook)
        ▼
AWS Glue — Script Editor (scriptNotebook)
        │  → Reads CSV from source bucket
        │  → Processes with PySpark
        ▼
S3 Bucket (dest-bucket-takeo)

        ↕  All stages monitored via CloudWatch Logs
```

---

## Repository Structure

```
aws-event-driven-etl/
│
├── README.md                        ← You are here
├── AWS Pipeline Setup Report.pdf    ← Full setup report (printable)
│
├── docs/
│   ├── setup-guide.md               ← Step-by-step setup instructions
│   └── architecture.md              ← Architecture overview and design decisions
│
├── iam/
│   └── policy-reference.md          ← IAM role and permissions breakdown
│
├── lambda/
│   ├── lambda_function.py           ← Lambda handler (Python 3.12)
│   └── README.md                    ← Lambda setup notes
│
└── glue/
    ├── scriptNotebook.py            ← AWS Glue PySpark ETL script
    └── README.md                    ← Glue setup notes
```

---

## Quick Start

> For the full walkthrough with code and steps, see [`docs/setup-guide.md`](docs/setup-guide.md) or open the [`AWS Pipeline Setup Report.pdf`](AWS%20Pipeline%20Setup%20Report.pdf).

1. **IAM** — Create role `source-bucket-takeo-role` with S3, Glue, and CloudWatch access
2. **S3** — Create source bucket `source-bucket-takeo`
3. **Lambda** — Create function `lambda2glue`, attach the role, add S3 trigger, deploy code
4. **Glue** — Attach role, create script `scriptNotebook`, save and run

---

## AWS Services Used

| Service           | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| Amazon S3         | Source upload bucket and processed output destination  |
| AWS Lambda        | Event listener — triggers Glue job on each file upload |
| AWS Glue          | ETL processor — reads, transforms, and writes data     |
| Amazon CloudWatch | Centralised logging and monitoring for all services    |
| AWS IAM           | Role-based access control across all services          |

---

## Key Files

| File                                                                   | Description                                                |
| ---------------------------------------------------------------------- | ---------------------------------------------------------- |
| [`AWS Pipeline Setup Report.pdf`](AWS%20Pipeline%20Setup%20Report.pdf) | Printable end-to-end setup report                          |
| [`lambda/lambda_function.py`](lambda/lambda_function.py)               | Lambda handler — extracts event data and triggers Glue     |
| [`glue/scriptNotebook.py`](glue/scriptNotebook.py)                     | Glue PySpark script — reads from S3, writes to destination |
| [`iam/policy-reference.md`](iam/policy-reference.md)                   | Breakdown of all IAM policies and why they're needed       |

---

## Requirements

- An active AWS account with permissions to create IAM roles, Lambda functions, and Glue jobs
- Source bucket (`source-bucket-takeo`) and destination bucket (`dest-bucket-takeo`) in the same AWS region
- CSV files with a header row for the Glue script to process correctly
