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
    BUTTON_TYPES["CONFIRM"]: ("Me", math.pi/6, lambda self: self.app.set_scene(OTPScene)), 
    BUTTON_TYPES["CANCEL"]: ("Back", math.pi*7/6, lambda self: self.app.minimise()), 
    BUTTON_TYPES["LEFT"]: ("Stats", math.pi*5/6, lambda self: self.app.set_scene(OTPScene)) 
  }
  async def background_task(self):
    return
  
  def update(self, delta):
    for button, action in self.actions.items():
      if self.app.button_states.get(button):
        action[self.ACTION_FN](self)
    self.app.button_states.clear()

  def draw(self, ctx):
    self.app.draw_background(ctx)
    
    for _, action in self.actions.items():
      ctx.save()
      ctx.rgb(1,1,1)
      rot = action[self.ACTION_ROTATION]
      m = action[self.ACTION_NAME]
      w = ctx.text_width(m)

      if rot > math.pi/2:
        off = -45-w
        rot -= math.pi
      else:
        off = 45
      ctx.rotate(rot)
      ctx.move_to(off,10)
      ctx.text(m)
      ctx.restore()


