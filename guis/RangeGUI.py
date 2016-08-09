from array2d import *

from random  import *
from Tkinter import *


# Range GUI allows to set a base value and the delta around the
# base value. These values may be then used for example in randomization.
class RangeGUI():
  
  def __init__(self, label="Range"):
    self.label = label
    self.base  = 0  # Base value
    self.delta = 10 # Delta value
  
  def layoutGUI(self, parent, heightmap):
    # Create the base level slider:
    frame = LabelFrame(parent, text=self.label)
    frame.pack(fill=X, padx=5, pady=5)
    
    bs = Scale(frame, orient=HORIZONTAL, label="Base level:")
    self.base_slider = bs
    bs["command"] = self.updateBase
    bs["from"] = -50
    bs["to"]   = +50
    bs.pack(fill=X)
    
    bs.set(self.base)
    
    # Create the delta value slider   
    ds = Scale(frame, orient=HORIZONTAL, label="Delta:")
    self.delta_slider = ds
    ds["command"] = self.updateDelta
    ds.pack(fill=X)
    ds["from"] = 0
    ds["to"]   = 100
    ds.set(self.delta)

  def updateBase(self, value):
    self.base = int(value)
  
  def updateDelta(self, value):
    self.delta = int(value)
    
  def getDelta(self):
    return self.delta
    
  def getBase(self):
    return self.base
    
  def copy(self):
    gui = RangeGUI()
    gui.base  = self.base
    gui.delta = self.delta
    return gui
