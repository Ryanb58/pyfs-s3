from fs.tempfs import TempFS
from fs_s3fs import S3FS


# Generate temp files to upload:
tempfs = TempFS()
for num in range(0, 100):
    with tempfs.open('file' + str(num), 'w') as fi:
        fi.write("I AM A FILE" * num)


# Connect to S3
s3fs = S3FS(
    'default',
    aws_access_key_id="minio",
    aws_secret_access_key="minio123",
    endpoint_url="http://localhost:9009")

# Print some info for us to use.
count = len(s3fs.listdir('/'))
print("File Count in S3: {}".format(count))
count = len(tempfs.listdir('/'))
print("File Count in tempfs: {}".format(count))

# Upload the files to S3
files = tempfs.listdir('/')
for fi in files:
    with s3fs.open(fi, 'w') as s3fi:
        s3fi.write(tempfs.open(fi, 'r').read())

count = len(s3fs.listdir('/'))
print("File Count in S3: {}".format(count))
