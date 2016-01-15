from random import *
from Tkinter import *

class LayerMode():
  def apply(self, val1, va2):
    pass
    
    
class AddLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 + val2
  
class SubtractLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 - val2
  
  
class MultiplyLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 * val2
    
class DivideLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 / val2
    

class DissolveLayerMode(LayerMode):
  def apply(self, val1, val2):
    rnd = randint(-1,1)
    if rnd < 0:
      return val1
    else:
      return val2
    
       
class MixLayerModel(LayerMode):
  def apply(self, val1, val2):
    return (val1 + val2) / 2
        
class LayersFactory():
  def __init__(self):
    prototypes = []
    self.prototypes = prototypes
    prototypes.append(RandomValuesLayer(0, ""))
  
  def getPrototypes(self):
    return self.prototypes

class Layer():
  
  # Constructor - may be overriden.
  def __init__(self, index, name):
    self.index = index
    self.name  = name
  
  # Layout gui interface for this layer controls.
  # Abstract method
  def layoutGUI(parent):
      pass
  
  def setMode(self, mode):
    self.mode = mode
  
  # Apply this layer to the stack. This method is called
  # if a previus layer in the stack returned this layer 
  # in the getNext method.
  # param stack      - The stack context for this layer.
  # param cumulative - 
  #   The 2d array of heights that is effect of the transformations done
  #   so far in the stack queue. This array should be altered - it will 
  #   be passed to the next layers down the stack.
  def apply(self, stack, cumulative):
    own_values = self.getValues(self, stack, previous, cumulative)
    
    for x in range(0, cumulative.width):
      for y in range(0, cumulative.height):
        own_val = own_values.get(x, y)
        cum_val = cumulative.get(x, y)
        new_val = self.mode.apply(own_val, cum_val)
        cumulative.set(x, y)
  
  # Get the values depending on the received context
  # This is a template method that should be overriden by 
  # inheriting classess.
  def getValues(self, stack, cumulative):
    pass
    
  # Get next layer to process in the stack.
  # This method should return the next layer that should
  # be applied to the stack. 
  def getNext(self, stack):
    return stack[self.index + 1]

  def getTypeName(self):
    return ""

  def getTypeDescription(self):
    return ""
  
  def copy(self):
    return None
    
  
class RandomValuesLayer(Layer):
  
  def __init__(self, index, name):
    Layer.__init__(self, index, name)
    
    self.base  = 0
    self.delta = 0
    
  def layoutGUI(self, parent):
    

    bs = Scale(parent, orient=HORIZONTAL, label="Base level:")
    self.base_slider = bs
    bs["command"] = self.updateBase
    bs.pack()
    bs["from"] = -50
    bs["to"]   = +50
    
    bs.set(self.base)
    
    delta_label = Label(parent, text="Delta:")
    delta_label.pack()
    
    ds = Scale(parent, orient=HORIZONTAL, label="Delta:")
    self.delta_slider = ds
    ds["command"] = self.updateDelta
    ds.pack()
    ds["from"] = 0
    ds["to"]   = 50
    ds.set(self.delta)
  
  def updateBase(self, value):
    print(value)
    self.base = value
  
  def updateDelta(self, value):
    self.delta = value
  
  def getTypeName(self):
    return "Random values layer."
    
  def getTypeDescription(self):
    return \
     "Layer with random heights distributed among the base  \
      value with a spread given by a delta value.  \
      \n\nThe selected seed is the seed of the random numbers \
      used internally by the python random number generator."
  
  def copy(self, index, name):
    return RandomValuesLayer(index, name)
  
    
      
