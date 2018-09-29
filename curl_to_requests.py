#!/usr/bin/env python3

import argparse
import re
import sys


class TargetNotFoundException(Exception):
    """Should be returned when no target url was found."""

    pass


def extract_target_url(command):
    """ Function used to find the target url of the curl command. """
    address_pattern = r"curl\s+'(.*?)'"
    address = re.search(address_pattern, command)
    if address is not None:
        return address.group(1)
    raise TargetNotFoundException("Target url not found in curl command.")


def extract_headers(command):
    """ Function used to extract headers from curl command. """
    headers_pattern = r"(-H\s*'((?![cC]ookie).*?)')"
    headers = re.findall(headers_pattern, command)

    results = {}
    for _, header in headers:
        k, v = header.split(":", 1)
        results[k] = v.strip()

    return results


def has_datas(command):
    """ Function to determine if there is data in the curl command, even if the datas are empty 
    or only if there is --data or -d without something next to it."""
    has_datas_pattern = r"(-d|--data)"
    has_datas = re.search(has_datas_pattern, command)
    return True if has_datas else False


def extract_datas(command):
    """ Function to get parameters of the curl command. """
    results = {}
    if not has_datas(command):
        return results
    datas_pattern = r"""(-d|--data)\s*['"](.*?)['"]"""
    datas = re.search(datas_pattern, command)

    if datas is not None:
        _, params = datas.groups()
        for p in params.split("&"):
            key, value = p.split("=", 1)
            results[key] = value

    return results

def extract_cookies(command):
    """ Function to extract cookies from curl command. """
    cookies_pattern = r"-H '[cC]ookie:(.*?)'"
    cookies = re.search(cookies_pattern, command)

    results = {}
    # TODO
    raise NotImplemented

def extract_http_verb(command):
    """ Function to extract the HTTP verb from a curl command. """
    http_verb_pattern = r"-X\s*([a-zA-Z]+)"
    verb = re.search(http_verb_pattern, command)

    if verb is not None:
        return str(verb.group(1)).lower()
    elif verb is None and has_datas(command):
        return "post"
    else:
        return "get"


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

    url = extract_target_url(command)
    headers = extract_headers(command)
    datas = extract_datas(command)
    verb = extract_http_verb(command)

    headers_str = (
        "headers = {}".format(
            str(headers)
        )
        if headers
        else ""
    )
    datas_str = f"datas = {str(datas)}" if datas else ""
    requests_str = f"requests.{verb}('{url}'%s%s)".strip() % (
        ", headers=headers" if headers else "",
        ", data=datas" if datas else "",
    )

    to_return = f"""
import requests

{headers_str}
{datas_str}
response = {requests_str}
    """.strip()
    return to_return

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    args = parser.parse_args()
    return args.command



if __name__ == "__main__":
    # extract_headers(CURL_EXAMPLES[0])
    # convert_curl_to_requests()
    command = parse_args(sys.argv[1:])
    print(convert_curl_to_requests(command))