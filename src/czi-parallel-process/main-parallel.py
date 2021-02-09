from pssh.clients import ParallelSSHClient
import boto3
from ec2 import EC2Instance
import os
from config import *
from datetime import datetime

print(f"Process started: {str(datetime.now())}")

launch_template_dict = {'LaunchTemplateId': "lt-055614c16e52565b4", 'Version': '4'}
ec2 = boto3.resource('ec2', region_name='us-west-1')
s3 = boto3.client('s3')


if UPLOAD_DIR:
    os.system(f'aws s3 cp --recursive {UPLOAD_DIR} s3://{S3_BUCKET}/{S3_CZI_DIR}')


def get_proc_image_command(image_loc):
    command_list = ['rm -f ~/data/raw/*', 'rm -f ~/data/output/*', f'aws s3 cp {image_loc} ~/data/raw/',
                    'echo "File Download Completed"',
                    'python ~/src/convert_all_files.py',
                    f'aws s3 cp --recursive ~/data/output/ {S3_OUTPUT_DIR}']
    command_string = ' && '.join(command_list)
    return command_string


instance_list = []
instance_ips = []

s3_file_list = []

file_objs = s3.list_objects(Bucket=S3_BUCKET, Prefix=S3_CZI_DIR)

for obj in file_objs['Contents']:
    if obj['Key'].endswith('.czi'):
        s3_file_list.append(f's3://{S3_BUCKET}/{obj["Key"]}')

print(f"Number of Images to Process: {len(s3_file_list)}")

for i in range(0, NUM_INSTANCES):
    inst = EC2Instance(ec2, launch_template_dict)
    inst.start_instance()
    instance_list.append(inst)

for instance in instance_list:
    instance.update_info()
    instance_ips.append(instance.public_dns)

print(f"Instances spun up: {len(instance_ips)}")

# key = load_private_key(SSH_KEY_LOC)
client = ParallelSSHClient(instance_ips, user='ubuntu', pkey=SSH_KEY_LOC, pool_size=NUM_INSTANCES)

output = client.run_command\
    ('rm -r ~/src && aws s3 cp --recursive s3://czi-process/src ~/src && echo "src files copied"')

print("Downloading Script Files...")

for host, host_output in output.items():
    for line in host_output.stdout:
        print("Host [%s] - %s" % (host, line))

while len(s3_file_list) > 0:

    print(f"------------------ Start: {str(datetime.now())}-----------------")

    s3_proc_list = list(map(get_proc_image_command, s3_file_list[:NUM_INSTANCES]))
    s3_file_list = s3_file_list[NUM_INSTANCES:]
    s3_proc_list += [''] * (NUM_INSTANCES - len(s3_proc_list))

    output = client.run_command('%s', host_args=tuple(s3_proc_list))
    for command in s3_proc_list:
        print(f"Running: {command}")

    # client.join(output)
    print(f"------------------ End: {str(datetime.now())}-----------------")
    for host, host_output in output.items():
        for line in host_output.stdout:
            print("Host [%s] - %s" % (host, line))

for inst in instance_list:
    inst.terminate_instance()

if DOWNLOAD_DIR:
    os.system(f"aws s3 cp --recursive {S3_OUTPUT_DIR} {DOWNLOAD_DIR}")

if EMPTY_S3:
    os.system(f"aws s3 rm --recursive s3://{S3_BUCKET}/{S3_CZI_DIR}")
    os.system(f"aws s3 rm --recursive {S3_OUTPUT_DIR}")

print(f"Process finished: {str(datetime.now())}")

