#!/usr/bin/env python3
import sys
import config
from datetime import datetime
import requests
from requests.exceptions import RequestException
from contextlib import closing
import jsonpath_rw
import re
import json

def log(*args):
  date = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
  print(date + " ".join(map(str, args)))

def get(url, headers, query_params):
  """ Returns the contents of the URL. If there is an error it is logged and None is returned. """
  try:
    log("Making request to {0}".format(url))
    with closing(requests.request("GET", url, headers=headers, params=query_params)) as response:
      if not is_ok(response):
        log("Request failed, code: {0} {1}".format(response.status_code, response.headers))
        return None
      log("Request successful, code: {0}".format(response.status_code))
      return response.content
  except RequestException as e:
    log("Request for '{0}' unsuccessful: {1}".format(url, str(e)))
    return None

def is_ok(response):
  content_type = response.headers['Content-Type'].lower()
  return (response.status_code == 200
          and content_type is not None)

def get_all():
  result = {'interviews':[]}
  params = {}
  after = ""
  mx = 10
  while after is not None and mx >= 0:
    if after:
      params['after'] = after

    res = get(config.URL, config.HEADERS, params)
    if not res:
      break
    content = json.loads(res)

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
  summaries = [match.value for match in jsonpath_rw.parse('$.interviews[*].interviewer.review.summary').find(data)]
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
