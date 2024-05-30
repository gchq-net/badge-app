from ..scene import Scene
from ..util import *
import math
from events.input import Buttons, BUTTON_TYPES

def goto_menu(self):
    from .menu_scene import GCHQMenuScene as MenuScene
    self.app.set_scene(MenuScene)

class OTPScene(Scene):
  ACTION_NAME = 0
  ACTION_ROTATION = 1
  ACTION_FN = 2
  actions = {
    BUTTON_TYPES["CANCEL"]: ("", 0, goto_menu ), 
  }
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.button_states = Buttons(self)
    self.otp_timer = 0
    self.otp_string = ""
    self.has_otp = False

  def set_otp_string(self, m):
     self.otp_string = m

  async def background_task(self):
    return
  
  def update(self, delta):
    for button, action in self.actions.items():
      if self.app.button_states.get(button):
        action[self.ACTION_FN](self)
    self.app.button_states.clear()
    if self.otp_timer <= 0:
        self.otp_timer = 30
        self.has_otp = False
    if self.has_otp:
        self.otp_timer -= delta/1000

  def draw(self, ctx):
    pi = math.pi
    ctx.save()
    self.app.draw_background(ctx)
    # ctx.rgb(0,0,0).arc(0,0,150, 0, 2*pi, 0).fill()

    # self.app.draw_logo_animated(ctx)

    # ctx.rgba(0,0,0,.5).arc(0,0,150, 0, 2*pi, 0).fill()
    # ctx.font_size -= 2

    # ctx.rgb(0,0,0)
    # roundtext(ctx, "GCHQ.NET", 100, True)
    theta=2*math.pi*self.otp_timer/30
    if self.has_otp:
        ctx.rgb(1,0,0).arc(0,0,120,0,theta,0).arc(0,0,115,theta,0,-1).fill()
    
    m = self.otp_string
    w = ctx.text_width(m)
    ctx.move_to(-w/2, 10)

    ctx.text(m)

    ctx.restore()