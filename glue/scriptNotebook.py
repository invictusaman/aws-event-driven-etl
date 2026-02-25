import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

# Receive arguments passed from Lambda
args = getResolvedOptions(sys.argv, ["VAL1", "VAL2"])

val1 = args["VAL1"]  # file_name
val2 = args["VAL2"]  # bucket_name

print("VAL1 (file_name):", val1)
print("VAL2 (bucket_name):", val2)

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Read the CSV file from the source S3 bucket
src_file = f"s3://{val2}/{val1}"
df = spark.read.format("csv").option("header", "true").load(src_file)
print("Read successful")

# Write the processed file to the destination S3 bucket
# NOTE: Update "dest-bucket-takeo" if your destination bucket has a different name
dest = f"s3://dest-bucket-takeo/{val1}"
df.write.mode("overwrite").option("header", "true").csv(dest)

print("Write successful")

# Finalize the Glue job
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
job.commit()
