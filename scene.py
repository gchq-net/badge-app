from app import App

class Scene:
  def __init__(self, app):
    self.app = app
  # When this function returns it is assumed the Scene is over
  async def background_task(self):
    pass

  def update(self, delta):
    pass

  def draw(self, ctx):
    pass
