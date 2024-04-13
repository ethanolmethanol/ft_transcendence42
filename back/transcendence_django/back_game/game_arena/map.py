class Map:
   def __init__(self): # TODO Map size and shape depends on number of player
      self.width = 900
      self.height = 500

   def update(self, newWidth, newHeight):
      self.width = newWidth
      self.height = newHeight

   def to_dict(self):
      return {
         'width': self.width,
         'height': self.height
      }
