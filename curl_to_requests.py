import requests
import click
import re


REGEX_ADDRESS = r"curl '[\w:\/\.0;9-]+'"
REGEX_HEADERS = r"-H '[\w\s:\/\.,+=;*\-()]+"
#
# @click.command()
# @click.argument('command')
def convert_curl_to_requests(command):
    """
    Take a curl as parameter and return the str of the python to implement.
    :param command:
    :return:
    """
    address = re.findall(REGEX_ADDRESS, command)[0].split(' ')[1].strip("'")
    headers = re.findall(REGEX_HEADERS, command)


    print(address)
    print(headers)
    return address


if __name__ == "__main__":

    TEST_COMMAND = "curl 'https://stackoverflow.com/questions/28568900/django-pagination-object-of-type-nonetype-has-no-len' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'referer: https://www.google.fr/' -H 'authority: stackoverflow.com' -H 'cookie: prov=50b62f78-637f-c6ff-3ad1-a64d03e675db; __qca=P0-1804862972-1508318898660; cc=bce0d12d6dbe4386a29c85993987db2e; _ga=GA1.2.472993284.1508318899; _gid=GA1.2.115529633.1513108052' --compressed"
    convert_curl_to_requests(TEST_COMMAND)