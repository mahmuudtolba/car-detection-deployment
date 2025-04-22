import boto3
import os

bucket_name = "mlops-udemy-course-aws"
s3 = boto3.client('s3')

def download_dir(local_path, model_name):
    s3_prefix = 'ml-models/'+model_name

    os.makedirs(local_path, exist_ok=True)
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
        if 'Contents' in result:
            for key in result['Contents']:
                s3_key = key['Key']

                local_file = os.path.join(local_path, os.path.relpath(s3_key, s3_prefix))
                # os.makedirs(os.path.dirname(local_file), exist_ok=True)

                s3.download_file(bucket_name, s3_key, local_file)


def upload_image_to_s3(file_name , s3_prefix = 'ml-images' ,object_name = None ):
    if object_name is None :
        object_name = os.path.basename(file_name)
    
    object_name = f"{s3_prefix}/{object_name}"
    s3.upload_file(file_name ,bucket_name , object_name )


    response = s3.generate_presigned_url('get_object' , 
                                         Params = {
                                             'Bucket' : bucket_name ,
                                             'Key' : object_name
                                         },
                                         ExpiresIn = 3600)
    
    return response

def upload_direct_image_to_s3( file , s3_prefix = 'ml-images' ,object_name = None ):
    if object_name is None :
        object_name = os.path.basename(file.name)
    
    object_name = f"{s3_prefix}/{object_name}"
    s3.upload_fileobj(file ,bucket_name , object_name )


    response = s3.generate_presigned_url('get_object' , 
                                         Params = {
                                             'Bucket' : bucket_name ,
                                             'Key' : object_name
                                         },
                                         ExpiresIn = 3600)
    
    return response