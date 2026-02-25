# Architecture Overview

## How the Pipeline Works

This pipeline follows an **event-driven architecture** — no manual intervention is needed once it's set up. Uploading a file to S3 automatically kicks off the entire chain.

---

## Component Breakdown

### Amazon S3 — Event Source

- **`source-bucket-takeo`** acts as the entry point
- Any file uploaded (PUT event) to this bucket fires an S3 notification to Lambda
- **`dest-bucket-takeo`** is the output destination where Glue writes processed files

### AWS Lambda — Orchestrator

- Function **`lambda2glue`** is triggered by the S3 event
- Extracts the file name and bucket name from the event payload
- Logs both to CloudWatch for traceability
- Calls the Glue API to start the ETL job, passing the file details as arguments

### AWS Glue — ETL Processor

- Script **`scriptNotebook`** receives the file details from Lambda
- Reads the CSV file from the source S3 bucket using Apache Spark
- Writes the output to the destination S3 bucket
- Job runs and logs are available in CloudWatch

### Amazon CloudWatch — Monitoring Layer

- Lambda logs: `/aws/lambda/lambda2glue`
- Glue logs: Available under each job run in the Glue console
- Both surfaces allow real-time monitoring of the pipeline

### AWS IAM — Access Control

- Role **`source-bucket-takeo-role`** is shared by both Lambda and Glue
- Grants the minimum required access: S3, Glue, and CloudWatch

---

## Data Flow

```
User uploads CSV
        │
        ▼
S3: source-bucket-takeo
        │  PUT Event Notification
        ▼
Lambda: lambda2glue
        │  Logs file_name + bucket_name → CloudWatch
        │  Calls glue.start_job_run(JobName="scriptNotebook")
        ▼
Glue: scriptNotebook
        │  Reads s3://source-bucket-takeo/{file_name}
        │  Processes with PySpark
        │  Writes to s3://dest-bucket-takeo/{file_name}
        │  Logs output → CloudWatch
        ▼
CloudWatch
        └── /aws/lambda/lambda2glue  (Lambda logs)
        └── Glue job run logs        (Glue logs)
```

---

## Key Design Decisions

| Decision                                    | Reason                                                                    |
| ------------------------------------------- | ------------------------------------------------------------------------- |
| Lambda as orchestrator (not direct S3→Glue) | Adds logging, flexibility, and error handling before triggering Glue      |
| Shared IAM role for Lambda and Glue         | Simplifies permission management for a single-team pipeline               |
| Arguments passed via `--VAL1` / `--VAL2`    | Glue job parameters allow the same script to process any file dynamically |
| CSV format in Glue script                   | Can be extended to Parquet, JSON, or other formats                        |
