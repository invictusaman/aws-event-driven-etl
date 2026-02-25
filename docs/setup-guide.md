# Setup Guide

Complete walkthrough for connecting **S3 → Lambda → AWS Glue** with CloudWatch monitoring.

---

## Step 1 — Create the IAM Role

The IAM role grants Lambda and Glue the permissions they need to interact with S3, CloudWatch, and each other.

1. Go to **AWS Console** → search **IAM** → click **Roles** → **Create Role**
2. Under **Trusted entity type**, select **AWS Service**
3. Under **Use case**, select **Lambda** → click **Next**
4. Search and attach the following policies:

   | Policy                     | Purpose                           |
   | -------------------------- | --------------------------------- |
   | `AmazonS3FullAccess`       | Read/write access to S3 buckets   |
   | `AWSGlueConsoleFullAccess` | Start and manage Glue jobs        |
   | `CloudWatchFullAccess`     | Write logs and monitor executions |

5. Click **Next** → enter Role name: **`source-bucket-takeo-role`**
6. Click **Create Role**

> See [`iam/policy-reference.md`](../iam/policy-reference.md) for a full breakdown of each policy.

---

## Step 2 — Create the S3 Source Bucket

This bucket is the entry point of the pipeline. Any file uploaded here will trigger the Lambda function.

1. Go to **AWS Console** → search **S3** → click **Create Bucket**
2. Enter Bucket name: **`source-bucket-takeo`**
3. Select your preferred **AWS Region**
4. Under **Block Public Access**, uncheck all options to allow public access
5. Acknowledge the public access warning and click **Create Bucket**

> **Note:** Ensure your destination bucket (`dest-bucket-takeo`) also exists in the same region before running the Glue job.

---

## Step 3 — Create the Lambda Function

### 3.1 — Create the Function

1. Go to **AWS Console** → search **Lambda** → click **Create Function**
2. Select **Author from scratch**
3. Enter Function name: **`lambda2glue`**
4. Set Runtime to **Python 3.12**
5. Under **Permissions** → expand **Change default execution role**
6. Select **Use an existing role** → choose **`source-bucket-takeo-role`**
7. Click **Create Function**

### 3.2 — Add S3 Trigger

1. Inside `lambda2glue`, click **Add Trigger**
2. Under Trigger configuration, select **S3**
3. Choose bucket: **`source-bucket-takeo`**
4. Leave Event type as **PUT** (triggers on file upload)
5. Acknowledge the notice and click **Add**

### 3.3 — Add the Function Code

1. Go to the **Code** tab inside `lambda2glue`
2. Open `lambda_function.py` and replace all existing code with the contents of [`lambda/lambda_function.py`](../lambda/lambda_function.py)
3. Click **Deploy**

> **Important:** The `JobName` in the code is set to `"scriptNotebook"`. This must exactly match the script name you save in AWS Glue (Step 5.2).

### 3.4 — What the Code Does

When a file is uploaded to S3, Lambda:

- Extracts the **file name** and **bucket name** from the S3 event
- Logs both values to **CloudWatch**
- Starts the Glue job (`scriptNotebook`), passing the file name and bucket name as arguments (`--VAL1`, `--VAL2`)

### 3.5 — Monitoring via CloudWatch

Lambda automatically sends all `print()` output to CloudWatch. You can view logs two ways:

**Option A — From Lambda Console:**

- Go to `lambda2glue` → **Monitor** tab → click **View CloudWatch Logs**

**Option B — From CloudWatch directly:**

1. Go to **AWS Console** → search **CloudWatch**
2. Navigate to **Logs** → **Log Groups**
3. Click on **`/aws/lambda/lambda2glue`**
4. Open the latest **Log Stream**
5. You will see entries showing the **bucket name** and **file name** for every upload

---

## Step 4 — Set Up AWS Glue

### 4.1 — Attach the IAM Role to Glue

1. Go to **AWS Console** → search **AWS Glue**
2. Click **Setup roles and users** (in the left sidebar)
3. Under **IAM role for AWS Glue**, select **Set an existing IAM role as the default**
4. Choose **`source-bucket-takeo-role`** from the dropdown
5. Under **Access to Amazon S3**, select **No additional access — Do not change permissions**
6. Click **Apply Changes**

### 4.2 — Create the Glue ETL Script

1. In AWS Glue, navigate to **ETL Jobs** → **Notebooks**
2. Click **Script Editor**
3. Replace all existing code with the contents of [`glue/scriptNotebook.py`](../glue/scriptNotebook.py)
4. **Save the script name as exactly: `scriptNotebook`** — this must match the `JobName` in the Lambda function
5. Click **Save**

### 4.3 — What the Script Does

The Glue script:

- Receives `VAL1` (file name) and `VAL2` (bucket name) from Lambda
- Reads the uploaded CSV file from `s3://{bucket_name}/{file_name}`
- Prints a confirmation that the read was successful
- Writes the processed file to `s3://dest-bucket-takeo/{file_name}`
- Prints a confirmation that the write was successful

### 4.4 — Monitor Glue Job Runs

1. In AWS Glue → **ETL Jobs** → click on `scriptNotebook`
2. Go to the **Runs** tab to see all triggered executions
3. Click any run to view its **CloudWatch logs** for detailed output

---

## End-to-End Flow

Once everything is set up:

1. Upload any **CSV file** to `source-bucket-takeo`
2. **Lambda** is automatically triggered and logs the file name and bucket name
3. **Glue job** (`scriptNotebook`) starts automatically with the file details
4. Glue reads the file from the source bucket and writes it to `dest-bucket-takeo`
5. All logs are available in **CloudWatch**
