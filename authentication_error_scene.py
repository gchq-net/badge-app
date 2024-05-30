from ..scene import Scene
from events.input import BUTTON_TYPES

class AuthenticationErrorScene(Scene):
  actions = [("Login", None), ("Me", None), ("Back", "Back"), ("Stats", "Stats")]
  buttons = [BUTTON_TYPES["RIGHT"], BUTTON_TYPES["CONFIRM"], BUTTON_TYPES["CANCEL"], BUTTON_TYPES["LEFT"]]
  async def background_task(self):
    return
  
  def update(self, delta):
    if self.app.button_states.get(BUTTON_TYPES["CANCEL"]):
      self.app.kill()
      self.app.button_states.clear()
    pass

  def draw(self, ctx):
    self.app.draw_background(ctx)
    
    ctx.save()
    ctx.rgb(1,0,0)
    msgs = ["Authentication", "Failure", "Call:", "GCHQ", "4247"]
    y = -30
    for msg in msgs:
        w = ctx.text_width(msg)
        ctx.move_to(-w/2, y)
        ctx.text(msg)
        y += 20

    ctx.restore()
