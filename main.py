#!/usr/bin/env python3
import sys
import config
from datetime import datetime
import requests
from requests.exceptions import RequestException
from contextlib import closing
import re
import json

_session = None

def log(*args):
  date = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
  print(date + " ".join(map(str, args)))

def get_session():
  global _session
  if _session is not None:
    return _session
  _session = requests.Session()
  _session.headers = config.HEADERS.copy()
  token = read_token()
  if token:
    setup_token(token)
  return _session

def setup_token(token):
  cookie = requests.cookies.create_cookie(
    domain='start.interviewing.io', name='token', value=token, path='/', secure=True)
  get_session().cookies.set_cookie(cookie)
  get_session().headers['authorization'] = "Bearer " + token

def authenticate():
  email, password = get_login_details()
  log("Logging in")
  response = post(config.LOGIN, {'email': email, 'password': password})
  token = None
  if response:
    if 'token' in response:
      token = response['token']
  if not token:
    log("Could not login")
    sys.exit(1)
  write_token(token)
  write_login_details(email, password)
  setup_token(token)

def read_token():
  try:
    with open(config.TOKEN) as file:
      return file.read().strip()
  except Exception as e:
    return None

def write_token(token):
  with open(config.TOKEN, 'w') as file:
    file.write(token)

def get_login_details():
  email,password = read_login_details()
  if email and password:
    return email, password
  email = input('Email: ')
  password = input('Password: ')
  return email, password

def read_login_details():
  try:
    with open(config.AUTH) as file:
      email = file.readline().strip()
      password = file.readline().strip()
      if email and password:
        return email,password
  except Exception as e:
    return None,None

def write_login_details(email, password):
  with open(config.AUTH, 'w') as file:
    file.write(email + '\n')
    file.write(password + '\n')

def get(url, query_params, retry=True):
  """ Returns the contents of the URL. If there is an error it is logged and None is returned. """
  try:
    log("Making request to {0}".format(url))
    with closing(get_session().get(url, params=query_params)) as response:
      if not is_ok(response):
        if response.status_code == 401:
          if retry:
            authenticate()
            return get(url, query_params, retry=False)
          else:
            log("Authentication failed: {0} {1}".format(response.status_code, response.headers))
        else:
          log("Request failed, code: {0} {1}".format(response.status_code, response.headers))
        return None
      log("Request successful, code: {0}".format(response.status_code))
      return response.json()
  except RequestException as e:
    log("Request for '{0}' unsuccessful: {1}".format(url, str(e)))
    return None

def post(url, body_json):
  try:
    log("Making request to {0}".format(url))
    with closing(get_session().post(url, json=body_json)) as response:
      if not is_ok(response):
        log("Request failed, code: {0} {1}\n{2}".format(
          response.status_code, response.headers, str(response.content, 'utf-8')))
        return None
      log("Request successful, code: {0}".format(response.status_code))
      return response.json()
  except RequestException as e:
    log("Request for '{0}' unsuccessful: {1}".format(url, str(e)))
    return None

def is_ok(response):
  content_type = response.headers['Content-Type'].lower()
  return (response.status_code == 200 and content_type is not None)

def get_all():
  result = {'interviews':[]}
  params = {}
  after = ""
  mx = 10
  while after is not None and mx >= 0:
    if after:
      params['after'] = after

    content = get(config.URL, params)
    if not content:
      break

    after = content['nextAfter']
    interviews = content['interviews']
    print("total count: %d, next after: %s, # interviews: %d" % (content['totalCount'],
      after, len(interviews)))
    print()
    result['interviews'].extend(content['interviews'])
    mx -= 1
  return result

def save(data):
  with open('history.json', 'w') as outfile:
    json.dump(data, outfile)

def summary(data):
  summaries = []
  for interview in data['interviews']:
    if config.PSUEDONYM and interview['interviewer']['pseudonym'] != config.PSUEDONYM:
      # skip interviews where you were the interviewee.
      continue
    if 'review' not in interview['interviewer']:
      # No feedback yet.
      continue
    summaries.append(interview['interviewer']['review']['summary'])

  with open('history.txt', 'w') as outfile:
    for summary in summaries:
      outfile.write(summary)
      outfile.write('\n----------------------------------------------------\n')
  print("Saved feedback for %d interviews" % len(summaries))

def main():
  history = get_all()
  save(history)
  summary(history)

if __name__ == '__main__':
  main()
