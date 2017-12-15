# curl-to-requests
A simple CLI tool which converts a curl command to a Python requests command.

## Features 

Requires Python3.5+

Supported features :
- all HTTP verbs
- headers
- datas

What's to come next ?  
I'll add features when I'll encounter more uses case working with curl. 
Stay tuned !

## Install : 

Clone the repository :  
`git clone git@github.com:sorasful/curl-to-requests-.git`  
then cd in the repository

Create (or not ) a virtualenv and then install dependencies.  
`pip install -r requirements.txt`

## Usage:

Usage:  
`./curl_to_requests.py """curl 'http://example.com/' -H 'Accept-Encoding: gzip, deflate'  --compressed"""`

which will output a string corresponding to a the Python code for the requests. Just import requests and copy/paste it. 

If you want to see some informations concerning the application just run :  
`./curl_to_requests --help`


Enjoy !
