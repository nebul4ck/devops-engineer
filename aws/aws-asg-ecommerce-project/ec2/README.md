## EC2 Cloudformation stack for Airflow in `vasquiat` account

- Validate the CloudFormation template
```
$ aws cloudformation validate-template \
--template-body file://cf-ec2-asg-template.yaml \
--profile lineagrafica
```

- Create the stack
```
$ aws cloudformation create-stack --stack-name lg-demo-docker-cf \
--template-body file://cf-ec2-asg-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagrafica
```

- Update the stack
```
$ aws cloudformation update-stack --stack-name lg-demo-docker-cf \
--template-body file://cf-ec2-asg-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagrafica
```

- Delete the stack
```
$ aws cloudformation delete-stack --stack-name lg-demo-docker-cf \
--profile lineagrafica
```
