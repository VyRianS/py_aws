#!/usr/bin/python3.6

import os
import boto3

s3 = boto3.resource('s3')

# TODO: Add internal function to check existance of bucket, object, or local dir

def s3_list_buckets():
    if len(list(s3.buckets.all())) == 0:
        print('WARNING: No S3 buckets available.')
        return 1
    else:
        bucket_list = []
        for bucket in s3.buckets.all():
            bucket_list.append(bucket.name)
        return bucket_list

def s3_list_bucket_objects(bucket_name):
    if len(list(s3.Bucket(bucket_name).objects.all())) == 0:
        print('WARNING: No objects in S3 bucket \'' + bucket_name + '\'.')
        return 1
    else:
        object_list = []
        for object in s3.Bucket(bucket_name).objects.all():
            object_list.append(object.key)
        return object_list

def s3_download_bucket_object(bucket_name, object_name, output_path, overwrite = False):
    if os.path.isdir(os.path.split(output_path)[0]) == False:
        print('FATAL: Local path \'' + os.path.split(output_path)[0] + ' does not exist.')
        return 1

    if os.path.isfile(output_path):
        if overwrite == False:
            print('FATAL: Local file \'' + output_path + '\' already exists.')
            return 1

    # Iterates through all the objects to find object_name.
    for object in s3.Bucket(bucket_name).objects.all():
        if object.key == object_name:
            s3.Object(bucket_name, object_name).download_file(output_path)
            print('\'' + object_name + '\' downloaded locally to \'' + output_path + '\'.')
            return 0

    # Object does not exist if code reaches this point.
    print('WARNING: Object \'' + object_name + \
          '\' not found in S3 bucket \'' + bucket_name + '\'.')
    return 1

if __name__ == '__main__':
    print(s3_list_buckets())
    print(s3_list_bucket_objects('py-aws-testing'))
    s3_download_bucket_object('py-aws-testing','asd.txt','/home/code/asd.txt')
