# AWS Glue Script — `scriptNotebook`

## What It Does

This PySpark script is triggered by the Lambda function whenever a file is uploaded to `source-bucket-takeo`. It:

1. Receives the **file name** and **bucket name** as arguments from Lambda
2. Reads the uploaded CSV file from the source S3 bucket
3. Writes the processed output to `dest-bucket-takeo`
4. Logs progress at each stage to CloudWatch

---

## Setup

Refer to **Step 4** in [`docs/setup-guide.md`](../docs/setup-guide.md) for full setup instructions.

Quick summary:

- Go to **AWS Glue** → **ETL Jobs** → **Notebooks** → **Script Editor**
- Paste the contents of `scriptNotebook.py`
- Save with the name **`scriptNotebook`** (must match exactly)

---

## Arguments

The script expects two arguments passed from Lambda:

| Argument | Value                     |
| -------- | ------------------------- |
| `--VAL1` | File name (S3 object key) |
| `--VAL2` | Bucket name               |

---

## Important Notes

- The destination bucket is hardcoded as `dest-bucket-takeo`. Update this if your bucket name differs.
- The script reads **CSV files with a header row**. Modify the `spark.read` format if your files are JSON, Parquet, etc.
- The script name **must be saved as `scriptNotebook`** to match the `JobName` in the Lambda function.

---

## Monitoring

- Go to **AWS Glue** → **ETL Jobs** → `scriptNotebook` → **Runs** tab
- Click any run to view logs and output in CloudWatch
