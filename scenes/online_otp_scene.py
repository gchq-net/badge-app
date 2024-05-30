from ..scene import Scene
from events.input import BUTTON_TYPES
from .otp_scene import OTPScene
from ..auth import *
import requests as re
from ..config import URL

    

class OnlineOTPScene(OTPScene):
    def __init__(self, *args):
        super().__init__(*args)
        self.otp_string = "Waiting for connection"

    async def background_task(self):
        from network import WLAN
        wlan=WLAN(WLAN.IF_STA)
        self.otp_string = "Waiting for connection"
        while True:
            print("online bacground")
            if not wlan.isconnected():
                self.otp_string = "Need WiFi"
                self.has_otp = False
                await asyncio.sleep(10)
                continue
            print("test")
            self.otp_string = "Fetching Codes"
            print("test2")
            otp = self.get_otp()
            print("test3")
            print("got otp", otp)
            if otp is not None:
                self.otp_string = str(otp)
                self.has_otp = True
                while self.has_otp:
                    await asyncio.sleep(1)
            
    
    def get_otp(self):
        print("test4")
        auth=get_badge_auth()
        print(auth)
        try:
            resp = re.post(URL + "/api/badge/otp/", json=auth)
            if resp.status_code in [200]:
                return resp.json()
            print(resp.status_code)
            print(resp.text)
        except Exception as e:
            import sys
            sys.print_exception(e)

            
