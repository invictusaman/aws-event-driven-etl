# Lambda Function — `lambda2glue`

## What It Does

This function is triggered automatically whenever a file is uploaded to `source-bucket-takeo`. It:

1. Extracts the **file name** and **bucket name** from the S3 event
2. Logs both values to **CloudWatch**
3. Starts the Glue ETL job (`scriptNotebook`) with the file details passed as arguments

---

## Setup

Refer to **Step 3** in [`docs/setup-guide.md`](../docs/setup-guide.md) for full setup instructions.

Quick summary:

- Runtime: **Python 3.12**
- Execution Role: **`source-bucket-takeo-role`**
- Trigger: **S3 PUT event** on `source-bucket-takeo`

---

## Important Note

The `JobName` value in `lambda_function.py` is hardcoded as `"scriptNotebook"`.

```python
response = glue.start_job_run(
    JobName="scriptNotebook",   # ← Must match your Glue script name exactly
    ...
)
```

If you rename the Glue script, update this value to match.

---

## CloudWatch Log Group

```
/aws/lambda/lambda2glue
```

Logs include the file name, bucket name, and Glue job run ID for every triggered execution.
