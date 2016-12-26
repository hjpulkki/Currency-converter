This folder contains the front end code. It can be uploaded to S3 with the following command:

aws s3 sync . s3://<BUCKET NAME> --acl public-read