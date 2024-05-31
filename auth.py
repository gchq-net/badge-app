def get_badge_mac():
  from network import WLAN
  print("test7")
  try:
    wlan = WLAN(WLAN.IF_STA)
    ret = "-".join([f"{b:02X}" for b in  wlan.config('mac')])
    print(ret)
    return ret
  except Exception as e:
    import sys
    sys.print_exception(e)

def get_badge_secret():
  try:
    from tildagon import HMAC
    mac = HMAC.digest(HMAC.HMAC_KEY1, "GCHQ.NET").hex()
    return mac
  except Exception as e:
    import sys
    sys.print_exception(e)

def get_badge_auth():
  print("test5")
  return {
    'mac_address': get_badge_mac(),
    'badge_secret': get_badge_secret(),
  }