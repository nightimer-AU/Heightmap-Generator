from __future__ import division

from array2d import *
from ..guis.InterpolationGUI import *
from ClampGUI         import *
from ClampGUI         import *

from utils   import *

from random  import *
from Tkinter import *

from noise   import *



# Layer class - acts simlarly to a layer in graphical editing programs.
class Layer():
  
  # Constructor - may be overriden.
  def __init__(self, name, orig=None):
    self.index = 0
    self.name  = name
    self.mode  = AddLayerMode() if orig==None else orig.mode
  
  def getName(self):
    return self.name
  
  def setIndex(self, index):
    self.index = index
  
  # Layout gui interface for this layer controls.
  # Abstract method
  def layoutGUI(self, parent, heightmap):
      pass
  
  def setMode(self, mode):
    self.mode = mode
  
  def getMode(self):
    return self.mode
  
  # Apply this layer to the stack. This method is called
  # if a previus layer in the stack returned this layer 
  # in the getNext method.
  # param stack      - The stack context for this layer.
  # param cumulative - 
  #   The 2d array of heights that is effect of the transformations done
  #   so far in the stack queue. This array should be altered - it will 
  #   be passed to the next layers down the stack.
  def apply(self, stack, cumulative):
    own_values = self.getValues(stack, cumulative)
    
    for x in range(0, cumulative.width):
      for y in range(0, cumulative.height):
        own_val = own_values.get(x, y)
        cum_val = cumulative.get(x, y)
        new_val = self.mode.apply(own_val, cum_val)
        cumulative.set(x, y, new_val)
  
  # Get the values depending on the received context
  # This is a template method that should be overriden by 
  # inheriting classess.
  def getValues(self, stack, cumulative):
    pass
    
  # Get next layer to process in the stack.
  # This method should return the next layer that should
  # be applied to the stack. 
  def getNext(self, stack):
    return stack.get(self.index + 1)

  def getTypeName(self):
    return ""

  def getTypeDescription(self):
    return ""
  
  def copy(self, name):
    return None


        

