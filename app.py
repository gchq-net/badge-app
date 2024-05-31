import app, asyncio, math
from .captures import * 
from system.eventbus import eventbus
from events.input import Buttons, BUTTON_TYPES
from system.notification.events import ShowNotificationEvent
from system.scheduler.events import RequestStopAppEvent
from .scenes import *
from .util import *
import wifi
 

class GCHQBadgeApp(app.App):
  def __init__(self):
    self.button_states = Buttons(self)
    self.animation_counter = 0
    self.back_time = 0
    self.current_scene_task = None

  def set_scene(self, scene):
    self.current_scene = scene(self)
    if self.current_scene_task:
      self.current_scene_task.cancel()
    self.current_scene_task = None
    if scene:
      print(self.current_scene)
      t = self.current_scene.background_task()
      print(t)
      self.current_scene_task = asyncio.create_task(t)
      
  def kill(self):
    if self.current_scene_task:
      self.current_scene_task.cancel()
      self.current_scene_task = None
    eventbus.emit(RequestStopAppEvent(self))
    
  async def background_task(self):
    print("background task started")
    asyncio.create_task(self.background_submit())
    self.set_scene(GCHQMenuScene)
    try:
      from tildagon import HMAC
    except:
      self.set_scene(ErrorScene)
      self.current_scene.set_err_msg("Update Badge")
    while True:
      await asyncio.sleep(1)

  async def background_submit(self):
    while True:
      if not wifi.status():
        wifi.connect()
        print("No WiFi")
        if not wifi.wait():
            await asyncio.sleep(2)
            continue
      capture = next_capture()
      if capture is None:
        print("No Captures")
        await asyncio.sleep(10)
        continue
      if (await try_submit_capture(capture)) != CaptureResult.SUCCESS:
        print("Failed to submit capture")
        await asyncio.sleep(10)
        continue
      else:
        print("Submitted capture")
        eventbus.emit(ShowNotificationEvent("Capture Submitted"))

  def update(self, delta):
    self.animation_counter += delta/1000
    if self.button_states.get(BUTTON_TYPES["CANCEL"]):
        self.back_time += delta / 1_000
    else:
        self.back_time = 0
    if self.back_time > 1:
        self.back_time = 0
        self.minimise()
        self.button_states.clear()

    if self.current_scene:
      self.current_scene.update(delta)
      return
    

  def draw(self, ctx):
    if self.current_scene:
      self.current_scene.draw(ctx)
      return
    self.draw_background(ctx)
    
  def draw_background(self, ctx):
    pi = math.pi
    ctx.save()
    ctx.rgb(0,0,0).arc(0,0,150, 0, 2*pi, 0).fill()

    self.draw_logo_animated(ctx)

    ctx.rgba(0,0,0,.5).arc(0,0,150, 0, 2*pi, 0).fill()
    ctx.font_size -= 2

    ctx.rgb(0,0,0)
    roundtext(ctx, "GCHQ.NET", 100, True)
    ctx.restore()

    
  def draw_otp(self, ctx):
    # ctx.rgb(0,0,0).arc(0,0,150,0,2*math.pi,0).fill()
    # from network import WLAN
    # wlan=WLAN(WLAN.IF_STA)
    # if not wlan.isconnected():
    #   m = "Wifi disconnected!"
    #   w = ctx.text_width(m)
    #   ctx.move_to(-w/2, 10)
    #   ctx.rgb(1,1,1).text()
    #   return
    # c
    pass


  def draw_logo_animated(self, ctx):
    legw = .12
    pi=math.pi
    rs = [(150, 0), (100, 1), (75, 0), (45, 1), (40, 0)]
    for r,c in rs:
      ctx.arc(0,0,r,0,2*pi,0)
      ctx.rgba(c,c,c, 1)
      ctx.fill()
    ctx.save()
    ctx.rotate(self.animation_counter * pi / 3)
    for i in range(3):
      ctx.begin_path()
      ctx.arc(0, 0, 105, i*pi*2/3, (i+legw)*pi*2/3, 0)
      ctx.arc(0, 0, 44, (i+legw)*pi*2/3, i*pi*2/3, -1)
      ctx.rgba(1, 1, 1, 1)
      ctx.fill()
    ctx.restore()
        

    ps = [(-30, 5), (-20, 14), (-12, 5), (-5, 5), (5, 10), (12, 10), (20, 6)]

    ctx.move_to(ps[0][0], ps[0][1])
    ctx.begin_path()
    for px, py in ps:
      ctx.line_to(px, py)
    for px, py in ps:
      ctx.line_to(-px, -py)
    
    ctx.line_to(-30, 5)

    ctx.rgba(1, 1, 1, 1)
    ctx.fill()
    

__app_export__ = GCHQBadgeApp
