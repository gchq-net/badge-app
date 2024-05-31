import async_helpers
import requests
from .config import URL
from .auth import *

async def nop(*args, **kwargs):
  pass

async def post(url, json={}):
  json.update(get_badge_auth())
  print(json)
  resp = await async_helpers.unblock(requests.post, nop, URL + url, json=json)
  return resp
