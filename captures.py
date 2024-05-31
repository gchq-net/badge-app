import os, requests, json
from .auth import *
from .api_requests import *

_captures = None
_capture_file = "gchq.net.json"

def next_capture():
  global _captures
  load_captures()
  if len(_captures) >= 1:
    return _captures[0]

def load_captures():
  global _captures
  try:
    with open(_capture_file, 'r') as f:
      _captures = json.load(f)
  except:
    pass
  if isinstance(_captures, list):
    return
  _captures = []

def pop_capture(capture):
  global _captures
  load_captures()
  if len(_captures) >= 1 and _captures[0] == capture:
    _captures.pop(0)
    save_captures()

def save_captures(retry=False):
  global _captures
  try:
    with open(_capture_file, 'w') as f:
      json.dump(_captures)
  except:
    try:
      os.remove(_capture_file)
    except:
      if not retry:
        save_captures(True)

class CaptureResult:
    SUCCESS = 1
    AUTHENTICATION_FAILURE = -3
    UNKNOWN_FAILURE = -2
    ERROR = -1

def try_submit_capture(capture):
  url = "/api/badge/capture/"
  data = {"capture":{"sn": capture[0], "rand": capture[1], "hmac": capture[2]}, "app_rev": "0.1.0", "fw_rev": os.uname()[2]}
  try:
    response = post(url, json=data)
    if response.status_code == 200 or response.status_code == 201:
      pop_capture(capture)
      return CaptureResult.SUCCESS
    if response.status_code == 403:
      return CaptureResult.AUTHENTICATION_FAILURE
    else:
      print("Returned not 200")
      print(response.status_code)
      print(response.text)
      return CaptureResult.UNKNOWN_FAILURE
  except Exception as e:
    import sys
    sys.print_exception(e)
    return CaptureResult.ERROR
