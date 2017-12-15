#!/usr/bin/env python
import click
import re


REGEX_ADDRESS = r"curl '[\w:\/\.0;9-]+'|-X ?POST\s?'?\s?[\w:\/]+'?"
REGEX_HEADERS = r"""(-H ?(?:'|")[\w\s\\\/\.,;:\-\+=()\*]+)"""
REGEX_DATAS = r"""(-d|--data)( ?'[\w\s{":\.,}]+')"""
REGEX_VERB = r"""-X [\w]+"""

@click.command()
@click.argument('command')
def convert_curl_to_requests(command):
    """
    Take a curl command enclosed in triple quotes as parameter and return the str of the python to implement directly copy and paste.
    IMPORTANT: Enclose your curl command in triple quotes just like in the example provided.
    Do not forget to import requests module when you try the result.

    Example :
    python3 curl_to_requests.py \"""curl 'http://example.com/' -H 'Accept-Encoding: gzip, deflate'  --compressed\"""

    will return :
    requests.get(url='http://example.com/',   headers={'Accept-\n  Encoding': 'gzip, deflate'}, )
    """

    address = ""
    verb = "get" # By default when you don't precise to curl we use get
    datas = ""
    headers = ""

    r_address = re.findall(REGEX_ADDRESS, command)
    if r_address:
        address = r_address[0].split(' ')[-1].strip("'")


    r_headers = re.findall(REGEX_HEADERS, command)
    if r_headers:
        headers_k_v = [header.split(': ') for header in r_headers]
        headers = {key.replace('-H ', '').replace('"', '').replace("'", ''): value.replace('"', '').replace("'", '') for key, value in  headers_k_v}
        headers_display = "headers={0}, ".format(headers)

    r_datas = [x[1] for x in re.findall(REGEX_DATAS, command)]
    if r_datas:
        datas = "data={0}, ".format(r_datas[0].replace("'", ''))

    r_verb = re.findall(REGEX_VERB, command)
    if r_verb:
        verb = r_verb[0].replace('-X ', '').lower()

    address_display = "'{0}', ".format(address if not None else "")
    output = "requests.{0}(url={1} {2} {3})".format(verb, address_display, datas if datas else "", headers_display if headers else "")

    print(output)
    return output


if __name__ == "__main__":
    convert_curl_to_requests()