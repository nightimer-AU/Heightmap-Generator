from .Layer import *
from utils  import *
from guis.RangeGUI import *
from guis.SeedingGUI  import *

class SimplexLayer(Layer):
    def __init__(self, name, orig=None):
        Layer.__init__(self, name, orig)
        self.scale = 1 # The amount of spread
        self.seed_gui    = SeedingGUI()                   if orig == None else orig.seed_gui
        self.range_gui   = RangeGUI()                     if orig == None else orig.range_gui
        self.scale_gui   = ScaleGUI("Scale",1,100)        if orig == None else orig.scale_gui
        self.clamp_gui   = ClampGUI("Clamping",0, 255)    if orig == None else orig.clamp_gui 
        
    def layoutGUI(self, parent, heightmap):
        self.seed_gui.layoutGUI(parent, heightmap)
        self.range_gui.layoutGUI(parent, heightmap)
        self.scale_gui.layoutGUI(parent, heightmap)
        self.clamp_gui.layoutGUI(parent, heightmap)
        
        
    def getValues(self, stack, cumulative):
        self.noise  = SimplexNoise()
        self.scale = self.scale_gui.getValue()
        
        w = cumulative.getWidth()
        h = cumulative.getHeight()
        
        arr2d = Array2D(w,h)
        arr2d.each(self.makeNoisy)
        
        return arr2d
        
    def makeNoisy(self, arr2d, x, y, orig): # The original will be 0 here always
        scale = float(self.scale_gui.getValue())
       
        seed = self.seed_gui.getSeed()
          
        offset = seed * arr2d.getWidth()

        val = self.noise.noise2d(x / scale + offset, y / scale)

        minimum = self.range_gui.getMinimum()
        maximum = self.range_gui.getMaximum()
        
        val = mapRange(val, 0, 1, minimum, maximum)

        is_clamping_enabled = self.clamp_gui.isEnabled()

        if is_clamping_enabled:
          
          max_val = self.clamp_gui.getTopValue();
          min_val = self.clamp_gui.getBottomValue();
          
          if not max_val < min_val: # Clamp only when possible
              val = clamp(val, min_val, max_val)
        
        return val
        
    def getTypeName(self):
        return "Simplex noise layer."
    
    def getTypeDescription(self):
      return "Layer whose values are generated using simplex noise algorithm."
    
    def copy(self, name):
        layer = SimplexLayer(name, self)
        return layer        
        
        
