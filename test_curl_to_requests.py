from curl_to_requests import (extract_target_url, TargetNotFoundException, 
        extract_headers, extract_datas, extract_http_verb, has_datas,convert_curl_to_requests)
import pytest


CURL_EXAMPLES = ["""curl 'https://docs.pytest.org/en/latest/' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://www.google.fr/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'Cookie: _ga=GA1.2.218880790.1538214405; _gid=GA1.2.1175981180.1538214405; __utma=169486132.218880790.1538214405.1538214405.1538214405.1; __utmc=169486132; __utmz=169486132.1538214405.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; _gat_rtfd=1; __utmb=169486132.2.10.1538214405' -H 'If-None-Match: W/"5baccc86-2b32"' -H 'If-Modified-Since: Thu, 27 Sep 2018 12:26:46 GMT' --compressed""",
"curl 'https://github.com/sorasful/curl-to-requests/settings/update_meta' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Origin: https://github.com' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://github.com/sorasful/curl-to-requests' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'Cookie: _ga=GA1.2.1194076640.1524999464; _octo=GH1.1.11962587.1524999464; user_session=atXJU7fNp6m26NYBLdGZtM-D0fLok6zytyJCo8A9zyT7x5Vs; __Host-user_session_same_site=atXJU7fNp6m26NYBLdGZtM-D0fLok6zytyJCo8A9zyT7x5Vs; logged_in=yes; dotcom_user=sorasful; has_recent_activity=1; tz=Europe%2FMadrid; _gh_sess=ZWhtLzloZVgySDdwbWRMakdwYVBVUGJpVXhwMGltS3ZQZlM0OGdwSWVQd3ZNWStydGZSc0J6RnAreXhHbGRPbXlSbkVFc09hQjhoZ29MOGNWMWg3dFNHS2FJcmlCMWlzZXNIaFRhdGNtNVVnMjZHeE1VQVdzaDcrNzQ4Z212bnJLZG9GWmxHZUEyMTd4OWI5V09md01pRmVuNS8xZ3JKTzdhTUNIQTZXK3lYUmswSldmWVpyMHc2WFQyd3k0QzhCZTNGaEU5OFFJRnNubzF1M3ZlZzRHdz09LS1yNFhJTkNPMmlndHYvMUxPNkRvUjN3PT0%3D--c88304cd1f3ad2bf369eca39f3fe7b24476c428d' --data 'utf8=%E2%9C%93&_method=put&authenticity_token=cMQnGAIRJ6CDxDD2N%2FoQXh4rnjYpO35ADiqeQPH7zCRvOVdMDlXIgkwMIM%2BwW8cwTYTBcmOUt6fHJstt4vbFEw%3D%3D&repo_description=A+CLI+tool+which+converts+a+curl+command+to+a+Python+requests+syntax.&repo_homepage=' --compressed", 
"curl 'https://www.google.fr/gen_204?s=web&t=aft&atyp=csi&ei=GE6vW-yaFIima8GTjIgF&rt=wsrt.427,aft.395,prt.395,sct.182' -X POST -H 'origin: https://www.google.fr' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36' -H 'content-type: text/plain;charset=UTF-8' -H 'accept: */*' -H 'referer: https://www.google.fr/' -H 'authority: www.google.fr' -H 'cookie: SID=dwZuamfmPKVP7D_r6enBc1lXoAOPIeG66pKPAuAkuTS4SATWToMmqsN4WiSRQAjCAlNaeQ.; HSID=A0p5kBPhGjN4_ajr-; SSID=AH4dqhh7du2tmE-oA; APISID=6FwY185Nl7AnTqS3/AsGVT46iQrsiulajZ; SAPISID=qH8mRpGETtrrPT3a/AZrTOojkmDdvk8SNU; OGPC=19008104-1:; NID=140=6vT-RnS7HK8VvuZtq81QeC97YWGHd7Mn0Zum5o0dyFj8CDfMOYJQxaNq4USrDq-RqOE24VfZKMTLSSxaAfNGSOBx6xsWXr_twePyYHb1XQeOYCnQSFDyxAl9agbzDPgSX5AujmjWjk0A1u4nnpUNRr90_2gCNioEtYscb9Bm2CkaAjgWhVEOtVv-cUz68CgHGGe6ehUoUnGKpLKNVlZpdAlb3QBAIq4UUO63uZmq7ry2En4hxqmD3eWUmrvebjhOueApIT4q-qUTdjzHSUwOsWbaECxYSBg2ASM; DV=Q-SsOBdddLkUQP_f7OZE3e4dV4ZMYhY; 1P_JAR=2018-09-29-10' -H 'content-length: 0' --compressed",
]               


def test_extract_target_url_success():
    curl_urls = [
    'https://docs.pytest.org/en/latest/',
    'https://github.com/sorasful/curl-to-requests/settings/update_meta',
    'https://www.google.fr/gen_204?s=web&t=aft&atyp=csi&ei=GE6vW-yaFIima8GTjIgF&rt=wsrt.427,aft.395,prt.395,sct.182',
      ]
    for ex, url in zip(CURL_EXAMPLES, curl_urls):
        assert extract_target_url(ex) == url

def test_extract_target_url_fail():
    with pytest.raises(TargetNotFoundException):
        assert extract_target_url("curl failed url")

def test_extract_headers_success():
    curl_no_headers = """curl 'https://docs.pytest.org/en/latest/' --compressed"""
    headers_example  = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.fr/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'If-None-Match': 'W/"5baccc86-2b32"',
        'If-Modified-Since': 'Thu, 27 Sep 2018 12:26:46 GMT',
        }

    assert extract_headers(CURL_EXAMPLES[0]) == headers_example
    assert extract_headers(curl_no_headers) == {}
    assert extract_headers("hfdsjfsdljk sdfskdfjsdf") == {}

def test_has_datas():
    curl1 = """curl 'http://fiddle.jshell.net/echo/html/' -H 'Origin: http://fiddle.jshell.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://fiddle.jshell.net/_display/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'msg1=wow&msg2=such' --compressed"""
    curl2 = """curl 'http://fiddle.jshell.net/echo/html/' -H 'Origin: http://fiddle.jshell.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://fiddle.jshell.net/_display/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --d 'msg1=wow&msg2=such' --compressed"""
    curl3 = """curl 'http://fiddle.jshell.net/echo/html/' -H 'Origin: http://fiddle.jshell.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://fiddle.jshell.net/_display/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data --compressed"""
    curl4 = """curl 'http://fiddle.jshell.net/echo/html/' -H 'Origin: http://fiddle.jshell.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://fiddle.jshell.net/_display/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive'   --compressed"""
                                        
    assert has_datas(curl1) == True
    assert has_datas(curl2) == True
    assert has_datas(curl3) == True
    assert has_datas(curl4) == False

def test_extract_datas():
    # should works with --data or -d
    curl_examples = ["""curl 'http://lolilol.net/' -H 'Origin: http://lolilol.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://fiddle.jshell.net/_display/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'params1=yes&params2=no' --compressed""",
                    """curl 'http://lolilol.net/' -H 'Origin: http://lolilol.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://fiddle.jshell.net/_display/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -d 'params1=yes&params2=no' --compressed""",]

    for curl in curl_examples:
        assert extract_datas(curl) == {'params1': 'yes', 'params2':'no'}


def test_extract_http_verb():
    curl_examples  = [ 
                """curl 'http://fiddle.jshell.net/echo/html/' --data 'msg1=wow&msg2=such' --compressed""",
                """curl 'http://fiddle.jshell.net/echo/html/' --compressed""",
                """curl 'http://fiddle.jshell.net/echo/html/' --data  --compressed""",
                """curl 'http://fiddle.jshell.net/echo/html/' -d  --compressed""",
                """curl 'http://fiddle.jshell.net/echo/html/' --data 'msg1=wow&msg2=such' -X PUT --compressed""",
                """curl 'http://fiddle.jshell.net/echo/html/' --data 'msg1=wow&msg2=such' -X delete --compressed""",
                """curl 'http://fiddle.jshell.net/echo/html/' -X PATCH --data 'msg1=wow&msg2=such' --compressed""",
                ]            
    https_verbs = ['post', 'get', 'post', 'post', 'put', 'delete', 'patch']
    
    for curl, verb in zip(curl_examples, https_verbs):
        assert extract_http_verb(curl) == verb

def test_extract_cookies():
    # TODO: add cookies
    pass

def test_convert_curl_to_request():
    command = """curl 'http://lolilol.net/' -H 'Origin: http://lolilol.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8'  -H 'Accept: */*'   --data    --compressed"""
    result = """
import requests

headers = {
    'Origin': 'http://lolilol.net',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept': '*/*',
}

response = requests.post('http://lolilol.net/', headers=headers)
    """.strip()

    # TODO make good looking
    assert convert_curl_to_requests(command) == result 