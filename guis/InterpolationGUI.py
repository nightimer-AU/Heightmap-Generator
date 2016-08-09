from array2d import *

from random  import *
from Tkinter import *


   
# Interpolation gui, that layers, which use interpolation have.
class InterpolationGUI():
  def __init__(self, label="Interpolation"):
    self.label = label
    self.mode  = 2
    self.resolution = 2
    self.mode_var   = IntVar()
    
  def layoutGUI(self, parent, heightmap):
    w = heightmap.getWidth()
    h = heightmap.getHeight()
    
    frame = LabelFrame(parent, text=self.label)
    frame.pack(fill=X, padx=5)
    
    res_scale = Scale(frame, label="Resolution:", from_=2, to=(min(w,h)-1), orient=HORIZONTAL)
    self.resolution_scale = res_scale
    res_scale["command"] = self.updateResolution
    res_scale.set(self.resolution)
    res_scale.pack(fill=X)
    
    Radiobutton(frame, text="Linear", variable=self.mode_var, value=1).pack()
    Radiobutton(frame, text="Sinusoidal", variable=self.mode_var, value=2).pack()
    
    self.mode_var.set(self.mode)
    
    
  def updateResolution(self, value):
    self.resolution = int(value)
    
  def createInterpolator(self):
    mode = self.mode_var.get()
    if mode == 1: return lerp()
    if mode == 2: return slerp()
    
  def getResolution(self):
    return self.resolution

  def copy(self):
    gui = InterpolationGUI(self.label)
    gui.resolution = self.resolution
    return gui

