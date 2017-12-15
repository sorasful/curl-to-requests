import requests
import click
import re


REGEX_ADDRESS = r"curl '[\w:\/\.0;9-]+'|-X ?POST\s?'?\s?[\w:\/]+'?"
REGEX_HEADERS = r"""(-H ?(?:'|")[\w\s\\\/\.,;:\-\+=()\*]+)"""
REGEX_DATAS = r"""(-d|--data)( ?'[\w\s{":\.,}]+')"""
REGEX_VERB = r"""-X [\w]+"""

# @click.command()
# @click.argument('command')
def convert_curl_to_requests(command):
    """
    Take a curl as parameter and return the str of the python to implement.
    :param command:
    :return:
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

    # TEST_COMMAND = "curl 'https://stackoverflow.com/questions/28568900/django-pagination-object-of-type-nonetype-has-no-len' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'referer: https://www.google.fr/' -H 'authority: stackoverflow.com' -H 'cookie: prov=50b62f78-637f-c6ff-3ad1-a64d03e675db; __qca=P0-1804862972-1508318898660; cc=bce0d12d6dbe4386a29c85993987db2e; _ga=GA1.2.472993284.1508318899; _gid=GA1.2.115529633.1513108052' --compressed"
    # TEST_COMMAND = """curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:3000/data """
    # TEST_COMMAND = """curl 'https://github.com/RRMoelker/django-markdownify' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.google.fr/' -H 'Cookie: _octo=GH1.1.1777018281.1508277971; logged_in=yes; dotcom_user=sorasful; _ga=GA1.2.1964303453.1508277971; tz=Europe%2FParis; user_session=ZsdmRQ9PsYDZ6rUrl-w4TVpBwvQODg1teb8enr6PLDnLhYSP; __Host-user_session_same_site=ZsdmRQ9PsYDZ6rUrl-w4TVpBwvQODg1teb8enr6PLDnLhYSP; _gh_sess=eyJzZXNzaW9uX2lkIjoiYzU3ZDcxOWJkOTZlYzZjNjRkNzRmMmI2NTQ2NjVkNmEiLCJsYXN0X3JlYWRfZnJvbV9yZXBsaWNhcyI6MTUxMzMyODgwNTY1NiwiY29udGV4dCI6Ii8iLCJsYXN0X3dyaXRlIjoxNTEzMjc5NTAwODg5LCJzcHlfcmVwbyI6InNvcmFzZnVsL2N1cmwtdG8tcmVxdWVzdHMtIiwic3B5X3JlcG9fYXQiOjE1MTMzMjg4MDV9--f5fd8fab08606e7779fc74a007e1e95acd143caf' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed"""
    TEST_COMMAND = """curl 'http://docs.python-requests.org/en/master/user/quickstart/'  --compressed"""
    convert_curl_to_requests(TEST_COMMAND)