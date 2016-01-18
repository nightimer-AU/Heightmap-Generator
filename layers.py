from array2d import *
from guis    import *

from random  import *
from Tkinter import *


# Layer mode represents operation that is done on the 
# the cumulative values of the current layer application.
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



# The layers factory is a kind of registry kind object
# that stores all the possible layer types in an array.        
class LayersFactory():
  def __init__(self):
    prototypes = []
    self.prototypes = prototypes
    prototypes.extend((
      RandomValuesLayer(""),
      RandomsInterpolatedLayer("")
    ))
  
  def getPrototypes(self):
    return self.prototypes


# The definition of a stack of layers used while generating
# the heightmap.
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
    



# Layer class - acts simlarly to a layer in graphical editing programs.
class Layer():
  
  # Constructor - may be overriden.
  def __init__(self, name):
    self.index = 0
    self.name  = name
    self.mode = AddLayerMode()
  
  def getName(self):
    return self.name
  
  def setIndex(self, index):
    self.index = index
  
  # Layout gui interface for this layer controls.
  # Abstract method
  def layoutGUI(parent, heightmap):
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

# Null object layer - used at the start of an application.
class DummyLayer(Layer):
  def __init__(self):
    Layer.__init__(self, "Dummy layer")


  
class RandomValuesLayer(Layer):
  
  def __init__(self, name):
    Layer.__init__(self, name)
    self.seed_gui       = SeedingGUI()
    self.random_gui = RandomizationGUI()
    
  def layoutGUI(self, parent, heightmap=None):
    self.seed_gui.layoutGUI(parent, heightmap)
    self.random_gui.layoutGUI(parent, heightmap)
  
  def getValues(self, stack, cumulative):
    w = cumulative.getWidth()
    h = cumulative.getHeight()
    array = Array2D(w, h)
    
    array.each(self.randomizeArrayELement)
    return array
  
  def randomizeArrayElement(self, x, y, element):
    upper = self.random_gui.base + self.random_gui.delta
    lower = self.random_gui.base - self.random_gui.delta
    return randint(lower, upper)
  
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

    
# Interpolated layer makes a <resolution> spaced
# array of random values, which it then interpolates 
# over to a bigger array using selected interpolation.
class RandomsInterpolatedLayer(RandomValuesLayer):
  def __init__(self, name):
    RandomValuesLayer.__init__(self, name)
    self.interpolate_gui  = InterpolationGUI()
    
  def layoutGUI(self, parent, heightmap=None):
    RandomValuesLayer.layoutGUI(self, parent, heightmap)
    self.interpolate_gui.layoutGUI(parent, heightmap)
    
  def getValues(self, stack, cumulative):
    res = self.interpolate_gui.resolution
    initial_array = Array2D(res, res)
    initial_array.each(self.randomizeArrayElement)    
    
    interoplation = self.interpolate_gui.createInterpolation()
    w = cumulative.getWidth()
    h = cumulative.getHeight()
    interpolated = initial_array.makeInterpolated(w,h, slerp())
    interpolated.each(self.roundArrayElement)
    return interpolated
    
  def roundArrayElement(self, x, y, value):
    return round(value)
  
    
  def getTypeName(self):
    return "Sine interpolated random layer "
    
  def getTypeDescription(self):
    return \
      "Sine interpolated layer makes a <resolution> spaced \
      array of random values, which it then interpolates \
      over to a bigger array using sinusoidal interpolation."

  def copy(self, name):
    return RandomsInterpolatedLayer(name)
  


