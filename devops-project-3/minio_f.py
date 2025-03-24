import yaml
import sys
import os
from minio import Minio
from minio.error import S3Error

def check_minio_bucket():
    with open('minio_config.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)

    access_key = yaml_data.get('access_key')
    secret_key = yaml_data.get('secret_key')
    bucket_name = yaml_data.get('bucket_name')
    url = yaml_data.get('url')

    client = Minio(url, access_key=access_key, secret_key=secret_key, secure=True)

    try:
        found = client.bucket_exists(bucket_name)

        if found:
            print(f"Access to {bucket_name} exist.")
            print("------------------------List of objects------------------------")
            objects = client.list_objects(bucket_name, recursive=True)
            for obj in objects:
                print(f"Object: {obj.object_name}, Size: {obj.size}, Midified: {obj.last_modified}")
        else:
            print(f"Access to {bucket_name} NOT exist.")
            sys.exit(1)
    except S3Error as err:
        print(f"Error: {err}")
        sys.exit(1)

def upload_to_minio():
    with open('minio_config.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)

    access_key = yaml_data.get('access_key')
    secret_key = yaml_data.get('secret_key')
    bucket_name = yaml_data.get('bucket_name')
    url = yaml_data.get('url')

    client = Minio(url, access_key=access_key, secret_key=secret_key, secure=True)

    backup_file_names = []
    with open('backup_file_names.txt', 'r') as file:
        backup_file_names = [line.strip() for line in file]

    for file_name in backup_file_names:
        file_path = f'/home/user/Desktop/DevOps/tasks/task2/backup/{file_name}'

        try:
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size

            with open(file_path, 'rb') as file_data:
                client.put_object(bucket_name, file_name, file_data, length=file_size)
            print(f'File {file_name} was success upload to Minio!')
        except FileNotFoundError:
            print(f'File {file_path} is not found.')
        except S3Error as e:
            print(f'Error Minio: {e}')

    print("------------------------List of objects------------------------")
    objects = client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        print(f"Object: {obj.object_name}, Size: {obj.size}, Midified: {obj.last_modified}")