import json
import pandas as pd
import boto3

json_path = input("Enter the path to the JSON file: ")
output_csv = input("Enter a name for the CSV file (e.g., output.csv): ")
bucket_name = input("Enter the S3 bucket name: ")
key = input("Enter the file name in S3 (e.g., output.csv): ")

with open(json_path, "r") as json_file:
    data = json.load(json_file)

df = pd.DataFrame(data)

df.to_csv(output_csv, index=False, encoding='utf-8')

s3 = boto3.client('s3')

with open(output_csv, "rb") as file:
    s3.upload_fileobj(file, bucket_name, key)

print(f"File {output_csv} successfully uploaded to Amazon S3! {bucket_name}")
