A simple app to show how to upload files to Blackblaze through a wep server.
The idea is to load multi files in the same request and make sure that they are written synchronously.

The wep server used here is flask.

If you happened to come across the Blackbaze documentation for python with boto3 library, this code will straight forward to understand.
If you didn't, give this link a look [blackblaze docs](https://www.backblaze.com/b2/docs/python.html) 

## Setup:
```
$ git clone https://github.com/alfatih-fdll-almola/chat-bot-for-Querying-banking-transactions.git
$ cd chat-bot-for-Quering-banking-Transaction
$ python3 -m venv venv
$ . venv/bin/activate
```
Install dependencies
```
$ (venv) pip install -r requirements.txt
```
run
```
$ (venv) python3 app.py
```
