#!/usr/bin/python3.6

import boto3

s3 = boto3.resource('s3')

if len(list(s3.buckets.all())) == 0:
    print('WARNING: No buckets available.')
else:
    for bucket in s3.buckets.all():
        print(bucket.name)

