#!/usr/bin/env python3
import auth
URL = "https://start.interviewing.io/api/interviews"

QUERY_PARAMS = {"after":""}

HEADERS = {
    'cookie': auth.cookie,
    'authorization': auth.authorization,
    'authority': "start.interviewing.io",
    'accept': "application/json, text/plain, */*",
    'cache-control': "no-cache",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    'referer': "https://start.interviewing.io/history",
    'Host': "start.interviewing.io",
    'Connection': "keep-alive",
    'pragma': "no-cache",
}

# curl 'https://start.interviewing.io/history'
# -H 'upgrade-insecure-requests: 1'
# -H 'dnt: 1'
# -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
# -H 'referer: https://start.interviewing.io/'
# -H 'accept-encoding: gzip, deflate, br'
# -H 'accept-language: en-US,en;q=0.9,az-AZ;q=0.8,az;q=0.7,fa-IR;q=0.6,fa;q=0.5'
# -H 'cookie: XXX