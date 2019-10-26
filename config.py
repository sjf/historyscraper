#!/usr/bin/env python3
import auth
LOGIN = "https://start.interviewing.io/auth/local"
URL = "https://start.interviewing.io/api/interviews"
TOKEN = ".token.txt"
AUTH = ".auth.txt"

HEADERS = {
    'Accept': "application/json, text/plain, */*",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    'referer': "https://start.interviewing.io/history",
    'Content-Type': "application/json;charset=UTF-8",
}

