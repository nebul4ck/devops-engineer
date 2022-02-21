## EC2 Cloudformation stack for Airflow in `vasquiat` account

- Validate the CloudFormation template
```
$ aws cloudformation validate-template \
--template-body file://cf-ec2-ddbb-instance-template.yaml \
--profile lineagraficaParis
```

- Create the stack
```
$ aws cloudformation create-stack --stack-name lg-demo-ddbb-instance-cf \
--template-body file://cf-ec2-ddbb-instance-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagraficaParis
```

- Update the stack
```
$ aws cloudformation update-stack --stack-name lg-demo-ddbb-instance-cf \
--template-body file://cf-ec2-ddbb-instance-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagraficaParis
```

- Delete the stack
```
$ aws cloudformation delete-stack --stack-name lg-demo-ddbb-instance-cf \
--profile lineagraficaParis
```
