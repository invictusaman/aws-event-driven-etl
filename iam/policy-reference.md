# IAM Role & Policy Reference

## Role: `source-bucket-takeo-role`

This role is used by both **AWS Lambda** and **AWS Glue**. It must be created before any other resource in this pipeline.

---

## Attached Policies

### 1. `AmazonS3FullAccess`

Grants full read and write access to all S3 buckets in the account.

**Used by:** Lambda (to read event metadata), Glue (to read source and write to destination)

Key permissions included:

- `s3:GetObject` — read files from source bucket
- `s3:PutObject` — write processed files to destination bucket
- `s3:ListBucket` — list objects in a bucket

---

### 2. `AWSGlueConsoleFullAccess`

Grants Lambda the ability to start, stop, and monitor Glue jobs.

**Used by:** Lambda (to call `glue.start_job_run`)

Key permissions included:

- `glue:StartJobRun` — trigger a Glue ETL job
- `glue:GetJobRun` — check the status of a job run
- `glue:GetJob` — retrieve job configuration details

---

### 3. `CloudWatchFullAccess`

Grants write access to CloudWatch Logs for monitoring and debugging.

**Used by:** Lambda (to write execution logs), Glue (to write job run logs)

Key permissions included:

- `logs:CreateLogGroup` — create a log group on first invocation
- `logs:CreateLogStream` — create a log stream per execution
- `logs:PutLogEvents` — write log entries

---

## How to Create the Role

1. Go to **IAM** → **Roles** → **Create Role**
2. Select trusted entity: **AWS Service** → **Lambda**
3. Attach all three policies listed above
4. Name the role: **`source-bucket-takeo-role`**
5. Click **Create Role**

> When setting up Glue (Step 4 in the setup guide), this same role is selected as the default Glue service role — no separate Glue role is needed.
