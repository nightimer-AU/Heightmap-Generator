from array2d import *

from random  import *
from Tkinter import *

# Layers GUI's 


class SeedingGUI():
  def __init__(self):
    self.seed_var = None
  
  def layoutGUI(self, parent, heightmap):
    if self.seed_var == None:
      seed = 0
    else:
      seed = int (self.seed_var.get())
      
    self.seed_var = StringVar()
    self.seed_var.set(seed)
    
    frame = Frame(parent)
    frame.pack()

    seed_label = Label(frame, text="Seed:")
    seed_label.pack(side=LEFT)        

    seed_entry = Entry(frame, textvariable=self.seed_var, width=6)    
    self.seed_entry = seed_entry
    seed_entry.pack(side=LEFT)
    
    randomize_button = Button(frame, text="Randomize")
    randomize_button["command"] = self.randomizeSeed
    randomize_button.pack(side=LEFT)
    
  def randomizeSeed(self):
    seed = randint(0, 1000)
    self.seed_var.set(seed)

class RandomizationGUI():
  
  def __init__(self):
    self.base  = 0
    self.delta = 10
  
  def layoutGUI(self, parent, heightmap):
    # Create the base level slider:
    bs = Scale(parent, orient=HORIZONTAL, label="Base level:")
    self.base_slider = bs
    bs["command"] = self.updateBase
    bs["from"] = -50
    bs["to"]   = +50
    bs.pack(fill=X)
    
    bs.set(self.base)
    
    # Create the delta value slider   
    ds = Scale(parent, orient=HORIZONTAL, label="Delta:")
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
    
class InterpolationGUI():
  def __init__(self):
    self.resolution = 1
    self.mode_var = IntVar()
    
  def layoutGUI(self, parent, heightmap):
    w = heightmap.getWidth()
    h = heightmap.getHeight()
    
    frame = LabelFrame(parent, text="Interpolation:")
    frame.pack(fill=X, padx=5)
    
    res_scale = Scale(frame, label="Resolution:", from_=1, to=(min(w,h)-1), orient=HORIZONTAL)
    self.resolution_scale = res_scale
    res_scale["command"] = self.updateResolution
    res_scale.set(self.resolution)
    res_scale.pack(fill=X)
    
    Radiobutton(frame, text="Linear", variable=self.mode_var, value=1).pack()
    Radiobutton(frame, text="Sinusoidal", variable=self.mode_var, value=2).pack()
    
  def updateResolution(self, value):
    self.resolution = int(value)
    
  def createInterpolation(self):
    mode = self.mode_var.get()
    if mode == 1: return lerp()
    if mode == 2: return slerp()
    
    
    
    
