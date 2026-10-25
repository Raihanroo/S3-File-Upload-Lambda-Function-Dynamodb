# S3 File Upload ও Lambda–DynamoDB প্রজেক্ট

এই প্রজেক্টে Python ও AWS Boto3 ব্যবহার করে দুটি কাজ করা যায়:

1. `my-assets/` ফোল্ডারের ফাইলগুলো Amazon S3 bucket-এ আপলোড করা।
2. AWS Lambda থেকে JSONPlaceholder API-এর user তথ্য নিয়ে Amazon DynamoDB table-এ সংরক্ষণ করা।

## প্রজেক্টের ফাইল

| ফাইল/ফোল্ডার | কাজ |
|---|---|
| `upload_to_s3.py` | `my-assets/`-এর ফাইলগুলো S3-তে আপলোড করে |
| `lambda_function_dynamodb.py` | API থেকে user তথ্য এনে DynamoDB-তে লেখে |
| `lambda_dynamodb_deploy.zip` | Lambda deployment package |
| `my-assets/` | S3-তে আপলোড করার নমুনা ফাইল |

## প্রয়োজনীয় জিনিস

- Python 3
- AWS account
- AWS CLI এবং AWS credentials
- Python-এর `boto3` package

## লোকাল সেটআপ

প্রজেক্ট ফোল্ডারে PowerShell বা terminal খুলে Boto3 ইনস্টল করুন:

```powershell
python -m pip install boto3
```

AWS CLI ইনস্টল করে credentials configure করুন:

```powershell
aws configure
```

আপনার AWS Access Key ID ও Secret Access Key নিজের কম্পিউটারে configure করুন। এগুলো কোনো source file, README বা GitHub-এ লিখবেন না।

## S3-তে ফাইল আপলোড

একটি S3 bucket-এর নাম ঠিক করুন। Bucket-এর নাম AWS-জুড়ে অনন্য হতে হবে। PowerShell-এ bucket নাম environment variable হিসেবে দিন:

```powershell
$env:S3_BUCKET_NAME = "আপনার-অনন্য-bucket-নাম"
python .\upload_to_s3.py
```

স্ক্রিপ্টটি `my-assets/` ফোল্ডারের ফাইলগুলো আপলোড করে। Bucket আগে থেকে না থাকলে এটি তৈরি করার চেষ্টা করে। AWS user বা role-এর উপযুক্ত S3 permission থাকতে হবে, যেমন bucket দেখার/তৈরি করার এবং object upload করার অনুমতি।

## Lambda ও DynamoDB সেটআপ

1. AWS DynamoDB-তে একটি table তৈরি করুন। Table-এর partition key হবে `id`, এবং এর ধরন হবে **Number**।
2. Lambda function তৈরি করে `lambda_function_dynamodb.py`-কে function code হিসেবে দিন।
3. Lambda configuration-এ `TABLE_NAME` environment variable যোগ করুন। এর মান দিন আপনার DynamoDB table-এর নাম।
4. Lambda execution role-এ ওই table-এ `dynamodb:PutItem` করার অনুমতি দিন।
5. Lambda function চালান। এটি `https://jsonplaceholder.typicode.com/users` থেকে user-দের তথ্য আনে এবং table-এ সংরক্ষণ করে।

Lambda-কে JSONPlaceholder API-তে network access থাকতে হবে। Lambda private VPC subnet-এ থাকলে বাইরের internet-এ যাওয়ার উপযুক্ত network setup প্রয়োজন হতে পারে।

## Deployment ZIP

`lambda_dynamodb_deploy.zip` ফাইলটি এই repository-তে দেওয়া আছে। Lambda Console-এ ZIP upload করার আগে নিশ্চিত করুন যে ZIP-এর ভেতরের handler code repository-র `lambda_function_dynamodb.py`-এর সঙ্গে মিলে। কোড পরিবর্তন করলে deployment ZIP-ও নতুন করে তৈরি করুন; ZIP-এ Python dependency প্রয়োজন হলে সেগুলোকেও package করতে হবে।

## নিরাপত্তা

- AWS credentials কখনো GitHub-এ push করবেন না।
- Credentials source code-এ hard-code না করে AWS CLI profile, environment configuration বা IAM role ব্যবহার করুন।
- প্রয়োজনের অতিরিক্ত AWS permission দেবেন না।

## সাধারণ সমস্যা

- **S3 bucket name সংক্রান্ত ত্রুটি:** নামটি অনন্য কি না এবং `S3_BUCKET_NAME` সঠিকভাবে সেট হয়েছে কি না দেখুন।
- **Access denied:** AWS identity-র S3/DynamoDB permission এবং Lambda execution role পরীক্ষা করুন।
- **DynamoDB table পাওয়া যাচ্ছে না:** `TABLE_NAME`-এর মান, table-এর region এবং Lambda region মিলিয়ে দেখুন।
