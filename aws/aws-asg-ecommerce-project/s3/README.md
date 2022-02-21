## S3 Cloudformation template for `vasquiat` account

- Validate the CloudFormation template
```
$ aws cloudformation validate-template \
--template-body file://cf-s3-alb-bucket-template.yaml \
--profile lineagraficaParis
```

- Create the stack
```
$ aws cloudformation create-stack --stack-name lg-demo-s3bucketalb-cf \
--template-body file://cf-s3-alb-bucket-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagraficaParis
```

- Update the stack
```
$ aws cloudformation update-stack --stack-name ld-demo-s3bucketalb-cf \
--template-body file://cf-s3-alb-bucket-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagraficaParis
```

- Delete the stack
```
$ aws cloudformation delete-stack --stack-name lg-demo-s3bucketalb-cf \
```
