import os
import sys
import shutil
import datetime
import paramiko
import boto3

# Configuration
SOURCE_DIR = '/path/to/source/directory'
DESTINATION_TYPE = 's3'  # 's3' for AWS S3, 'ssh' for SSH server
S3_BUCKET_NAME = 'your-s3-bucket-name'
S3_DESTINATION_PREFIX = 'backup/'  # Prefix for backup files in S3 bucket
SSH_HOST = 'your-ssh-host'
SSH_PORT = 22
SSH_USERNAME = 'your-ssh-username'
SSH_PASSWORD = 'your-ssh-password'
SSH_DESTINATION_DIR = '/path/to/ssh/destination/directory'
REPORT_FILE = 'backup_report.txt'

# Function to perform backup to S3
def backup_to_s3():
    try:
        session = boto3.Session()
        s3 = session.resource('s3')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file_name = f'backup_{timestamp}.zip'
        backup_file_path = os.path.join('/tmp', backup_file_name)
        shutil.make_archive(os.path.splitext(backup_file_path)[0], 'zip', SOURCE_DIR)
        s3.meta.client.upload_file(backup_file_path, S3_BUCKET_NAME, f'{S3_DESTINATION_PREFIX}{backup_file_name}')
        os.remove(backup_file_path)
        return True, f'Successfully backed up to S3 bucket {S3_BUCKET_NAME}'
    except Exception as e:
        return False, f'Failed to backup to S3: {str(e)}'

# Function to perform backup via SSH
def backup_via_ssh():
    try:
        transport = paramiko.Transport((SSH_HOST, SSH_PORT))
        transport.connect(username=SSH_USERNAME, password=SSH_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file_name = f'backup_{timestamp}.zip'
        backup_file_path = os.path.join('/tmp', backup_file_name)
        shutil.make_archive(os.path.splitext(backup_file_path)[0], 'zip', SOURCE_DIR)
        sftp.put(backup_file_path, os.path.join(SSH_DESTINATION_DIR, backup_file_name))
        sftp.close()
        transport.close()
        os.remove(backup_file_path)
        return True, f'Successfully backed up to SSH server {SSH_HOST}'
    except Exception as e:
        return False, f'Failed to backup to SSH server: {str(e)}'

# Main function
def main():
    if DESTINATION_TYPE == 's3':
        success, message = backup_to_s3()
    elif DESTINATION_TYPE == 'ssh':
        success, message = backup_via_ssh()
    else:
        print("Invalid destination type specified")
        sys.exit(1)

    with open(REPORT_FILE, 'a') as report_file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_file.write(f'{timestamp}: {"Success" if success else "Failure"} - {message}\n')

if __name__ == "__main__":
    main()
