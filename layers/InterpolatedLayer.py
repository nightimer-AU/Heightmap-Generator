from .RandomValuesLayer import RandomValuesLayer

from guis.InterpolationGUI import *    
from guis.ClampGUI         import *
from utils								 import *   

# Interpolated layer makes a <resolution> spaced
# array of random values, which it then interpolates 
# over to a bigger array using selected interpolation.
class InterpolatedLayer(RandomValuesLayer):
  def __init__(self, name, orig=None):
    RandomValuesLayer.__init__(self, name, orig)
    self.interpolate_gui  = InterpolationGUI() if orig == None else orig.interpolate_gui
    self.clamp_gui        = ClampGUI()         if orig == None else orig.clamp_gui
    
  def layoutGUI(self, parent, heightmap=None):
    RandomValuesLayer.layoutGUI(self, parent, heightmap)
    self.interpolate_gui.layoutGUI(parent, heightmap)
    self.clamp_gui.layoutGUI(parent, heightmap)
    
  def getValues(self, stack, cumulative):
    res = self.interpolate_gui.getResolution()
    initial_array = Array2D(res, res)
    seed = self.seed_gui.getSeed()
    setSeedNumber(seed)
    initial_array.each(self.randomizeArrayElement)    
    
    interoplator = self.interpolate_gui.createInterpolator()
    w = cumulative.getWidth()
    h = cumulative.getHeight()
    interpolated = initial_array.makeInterpolated(w,h, interoplator)
    
    interpolated.each(self.roundArrayValues)
    
    is_clamped = self.clamp_gui.isEnabled()
    if is_clamped:
      interpolated.each(self.clampArrayValues)
      
    
    return interpolated
   

  def randomizeArrayElement(self, x, y, value):
    base = self.range_gui.getBase()
    delta = self.range_gui.getDelta()
    min = base - delta
    max = base + delta
    return getNextSeedInt(min, max)

  def roundArrayValues(self, x, y, value):
    return round(value)
  
  def clampArrayValues(self, x, y, value):
    top = self.clamp_gui.getTopValue()
    btm = self.clamp_gui.getBottomValue()
    
    if value > top:
      return top
    elif value < btm:
      return btm
    else: return value
    
    
  def getTypeName(self):
    return "Interpolated layer "
    
  def getTypeDescription(self):
    return \
      "Sine interpolated layer makes a <resolution> spaced \
      array of random values, which it then interpolates \
      over to a bigger array using sinusoidal interpolation."

  def copy(self, name):
    layer = InterpolatedLayer(name, self)
    return layer
  
