Requirements:
* Python3
* Python3-pip
* awscli


1. Create $HOME/.aws/mfa_credentials file. Set your aws_access_key_id and aws_secret_access_key values
```
[your-profile]
aws_access_key_id=AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
2. Create /usr/local/bin/awslogin (or $HOME/.local/bin/awslogin) script and set the exec permissions.
```
#!/usr/bin/python3
2# -*- coding: utf-8 -*-
3import re
4import sys
5from mfa_tools.main import main
6
7if __name__ == '__main__':
8    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
9    sys.exit(main())
```

```
sudo chmod a+x /usr/local/bin/awslogin
```

3. Install python aws_mfa_tools library
```
pip3 install aws-mfa-tools
```
4. And this is how it is used:
```
awslogin --profile <gateway_account>
```
5. Finally, test that the authentication is working:
```
aws ec2 describe-instances --profile obes-dev
```