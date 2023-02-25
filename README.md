# transaction-processor

Chalice was used for this project [https://aws.github.io/chalice/](https://aws.github.io/chalice/)

## Requirements

* python 3.9
* A account in AWS

## Install
clone project and change to created directory.
```
$ git clone https://github.com/ghap16/transaction-processor.git
$ cd transaction-processor
```

Inside the new directory you will see a structure like this.
```
transaction-processor
│   README.md
│   .gitignore    
│
└───assets
│   │   transaction_summary.json
│   │   transaction-example1.csv
│   │   ...
│
└───src
    │   │   config.json   
    └───.chalice
    │   │   config.json
    │   │   policy-dev.json
    │   
    └───chalicelib
    │   │   ...
    │   
    └───tests
    │   │   ...
    │   
    │   app.py
    │   pytest.ini
    │   requirements-dev.txt
    │   requirements.txt
    │   ...

```


Create virtual environment.

```
$  python3 -m venv venv
```

Install requirements.
```
$  pip install -r requirements-dev.txt
$  pip install -r requirements.txt
```

## Configuration

### Verify email
In order to send and receive email within the sandbox, it is necessary to verify the email in AWS SES [https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html](https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html)

### Config Bucket and emails
You need to have a bucket and set that bucket in the environment variables inside the *src/chalicelib/.chalice/config.json* file. In that same file is the configuration for email_to and email_from, these emails should be previously verified in AWS SES

### Upload template
Upload the *assets/transaction-summary.html* file to the configured bucket.

## Run

Configure your aws credentials in *~/.aws/config*.

Go to src directory.
```
$  cd src
```

### local
Run following command
```
$  chalice local --stage dev
```

### Deploy
Run following command
```
$  chalice deploy --stage dev
```

When finished, it will return something like the following:

```
	Creating deployment package.
    Updating policy for IAM role: transaction-processor-dev-api_handler
    Updating lambda function: transaction-processor-dev
    Updating rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-east-1:579314821033:function:transaction-processor-dev
      - Rest API URL: https://whmpk53c6j.execute-api.us-east-1.amazonaws.com/api/
```


## Test
Inside the assets directory there is a postman collection, with this it can be loaded and tested by changing only a few variables according to the ones you have.


## Develop

### UnitTest
```
$ pytest
```
### Sorting and Formatting
```
$ isort .
$ black .
```

