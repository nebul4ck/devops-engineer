## EFS Shared Cloudformation template for `vasquiat` account

- Validate the CloudFormation template
```
$ aws cloudformation validate-template \
--template-body file://efs-cf-template.yaml \
--profile vasquiat
```

- Create the stack
```
$ aws cloudformation create-stack --stack-name vasquiat-efsvasquiat-cf \
--template-body file://cf-efs-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile vasquiat
```

- Update the stack
```
$ aws cloudformation update-stack --stack-name vasquiat-efsvasquiat-cf \
--template-body file://cf-efs-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile vasquiat
```

- Delete the stack
```
$ aws cloudformation delete-stack --stack-name vasquiat-efsshared-cf \
--profile vasquiat
```
