## VPC (network layer) Cloudformation template for demo purpose.

- Validate the CloudFormation template
```
$ aws cloudformation validate-template \
--template-body file://cf-net-layer-template.yaml \
--profile lineagraficaParis
```

- Create the stack
```
$ aws cloudformation create-stack --stack-name lg-as-network-layer-demo-cf \
--template-body file://cf-net-layer-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagraficaParis
```

- Update the stack
```
$ aws cloudformation update-stack --stack-name lg-as-network-layer-demo-cf \
--template-body file://cf-net-layer-template.yaml \
--parameters file://parameters/parameters.json \
--tags file://tags/tags.json \
--profile lineagraficaParis
```

- Delete the stack
```
$ aws cloudformation delete-stack --stack-name lg-as-network-layer-demo-cf
```
