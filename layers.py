from array2d import *

from random  import *
from Tkinter import *

class LayerMode():
  def apply(self, val1, va2):
    pass
  
  def getName(self):
    return ""
    
  @staticmethod
  def fromName(name):
    if name == "Add":      new_mode = AddLayerMode()
    if name == "Subtract": new_mode = SubtractLayerMode()
    if name == "Multiply": new_mode = MultiplyLayerMode()
    if name == "Divide":   new_mode = DivideLayerMode()
    if name == "Dissolve": new_mode = DissolveLayerMode()
    if name == "Mix":      new_mode = MixLayerModel()
    return new_mode
    
class AddLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 + val2

  def getName(self):
    return "Add"
    
  
class SubtractLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 - val2
  
  def getName(self):
    return "Subtract"

class MultiplyLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 * val2
    
  def getName(self):
    return "Multiply"

    
class DivideLayerMode(LayerMode):
  def apply(self, val1, val2):
    return val1 / val2
    
  def getName(self):
    return "Divide"


class DissolveLayerMode(LayerMode):
  def apply(self, val1, val2):
    rnd = randint(-1,1)
    if rnd < 0:
      return val1
    else:
      return val2
    
  def getName(self):
    return "Dissolve"

       
class MixLayerModel(LayerMode):
  def apply(self, val1, val2):
    return (val1 + val2) / 2
        
  def getName(self):
    return "Mix"

        
class LayersFactory():
  def __init__(self):
    prototypes = []
    self.prototypes = prototypes
    prototypes.append(RandomValuesLayer(""))
  
  def getPrototypes(self):
    return self.prototypes


class LayerStack():
  def __init__(self):
    self.layers = []
    
  def getNext(self, idx):
    return self.get(idx + 1)    
    
  def get(self, idx):
    try:
      return self.layers[idx]
    except:
      return None
  
  def append(self, layer):
    self.layers.append(layer)
    

class Layer():
  
  # Constructor - may be overriden.
  def __init__(self, name):
    self.index = 0
    self.name  = name
    self.mode = AddLayerMode()
  
  def setIndex(self, index):
    self.index = index
  
  # Layout gui interface for this layer controls.
  # Abstract method
  def layoutGUI(parent):
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
  
  def copy(self):
    return None
    
class DummyLayer(Layer):
  def __init__(self):
    Layer.__init__(self, "Dummy layer")
  
class RandomValuesLayer(Layer):
  
  def __init__(self, name):
    Layer.__init__(self, name)
    
    self.base  = 0
    self.delta = 10
    
    
  def layoutGUI(self, parent):
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
    ds["to"]   = 10
    ds.set(self.delta)
  
  def updateBase(self, value):
    self.base = int(value)
  
  def updateDelta(self, value):
    self.delta = int(value)
  
  def getTypeName(self):
    return "Random values layer."
    
  def getTypeDescription(self):
    return \
     "Layer with random heights distributed among the base  \
      value with a spread given by a delta value.  \
      \n\nThe selected seed is the seed of the random numbers \
      used internally by the python random number generator."
  
  def copy(self, name):
    return RandomValuesLayer(name)
  
    
  def getValues(self, stack, cumulative):
    w = cumulative.getWidth()
    h = cumulative.getHeight()
    array = Array2D(w, h)
    array.each(self.randomize)
    
    print("array")
    print(array)
    return array
    
    
    
  def randomize(self, x, y, element):
    upper = self.base + self.delta
    lower = self.base - self.delta
    return randint(lower, upper)
    
    
    
    
      
