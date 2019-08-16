from Layer import Layer

from guis.SeedingGUI import SeedingGUI
from guis.RangeGUI   import RangeGUI
from array2d 				 import *
from utils					 import *

# Layer with random values
class RandomValuesLayer(Layer):
  
  def __init__(self, name, orig=None):
    Layer.__init__(self, name, orig)
    self.seed_gui   = SeedingGUI() if orig == None else orig.seed_gui
    self.range_gui  = RangeGUI()   if orig == None else orig.range_gui
    
  def layoutGUI(self, parent, heightmap=None):
    self.seed_gui.layoutGUI(parent, heightmap)
    self.range_gui.layoutGUI(parent, heightmap)
  
  def getValues(self, stack, cumulative):
    w = cumulative.getWidth()
    h = cumulative.getHeight()
    array = Array2D(w, h)
    
    seed = self.seed_gui.getSeed()
    setSeedNumber(seed)
    
    array.each(self.randomize)
    return array
  
  def randomize(self, arr2d, x, y, element):
    minimum = self.range_gui.getMinimum()
    maximum = self.range_gui.getMaximum()
    
    return getNextSeedInt(minimum, maximum)
  
  def getTypeName(self):
    return "Random values layer."
    
  def getTypeDescription(self):
    return \
     "Layer with random heights distributed among the base  \
      value with a spread given by a delta value.  \
      \n\nThe selected seed is the seed of the random numbers \
      used internally by the python random number generator."
    
  def copy(self, name):
    layer = RandomValuesLayer(name, self)
    layer.seed_gui   = self.seed_gui.copy()
    layer.range_gui = self.range_gui.copy() 
    return layer

