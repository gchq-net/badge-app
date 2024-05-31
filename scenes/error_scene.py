from ..scene import Scene
from events.input import BUTTON_TYPES
# from .offline_otp_scene import OfflineOTPScene as OTPScene
from .online_otp_scene import OnlineOTPScene as OTPScene
import math

class GCHQMenuScene(Scene):
  ACTION_NAME = 0
  ACTION_ROTATION = 1
  ACTION_FN = 2
  actions = {
    BUTTON_TYPES["RIGHT"]: ("Login", -math.pi/6, lambda self: self.app.set_scene(OTPScene)), 
    #BUTTON_TYPES["CONFIRM"]: ("Me", math.pi/6, lambda self: self.app.set_scene(OTPScene)), 
    BUTTON_TYPES["CANCEL"]: ("Back", math.pi*7/6, lambda self: self.app.minimise()), 
    #BUTTON_TYPES["LEFT"]: ("Stats", math.pi*5/6, lambda self: self.app.set_scene(OTPScene)) 
  }
  async def background_task(self):
    return
  
  def update(self, delta):
    for button, action in self.actions.items():
      if self.app.button_states.get(button):
        action[self.ACTION_FN](self)
    self.app.button_states.clear()

  def set_err_msg(self, msg):
    self.err_msg = msg

  def draw(self, ctx):
    self.app.draw_background(ctx)
    ctx.rgb(1,0,0)
    w = ctx.text_width(self.err_msg)
    ctx.text(self.err_msg, -w/2, -10)



