from .Layer import *


class SimplexLayer(Layer):
    def __init__(self, name, orig=None):
        Layer.__init__(self, name, orig)
        self.spread = 1 # The amount of spread
        self.scale_gui   = ScaleGUI("Scale",1,255)        if orig == None else orig.scale_gui
        self.clamp_gui   = ClampGUI("Clamping",-127, 127) if orig == None else orig.clamp_gui 
        
    def layoutGUI(self, parent, heightmap):
        self.scale_gui.layoutGUI(parent, heightmap)
        self.clamp_gui.layoutGUI(parent, heightmap)
        self.spread_gui.layoutGUI(parent, heightmap)
        
    def getValues(self, stack, cumulative):
        self.noise  = SimplexNoise()
        self.spread = self.scale_gui.getValue()
        
        w = cumulative.getWidth()
        h = cumulative.getHeight()
        
        arr2d = Array2D(w,h)
        arr2d.each(self.makeNoisy)
        
        return arr2d
        
    def makeNoisy(self, x, y, orig): # The original will be 0 here always
        scale = self.scale_gui.getValue()
        
        #print("Scale is" + str(scale))
        val = int(self.noise.noise2d(x / scale,y / scale))
        
        max_val = self.clamp_gui.getTopValue();
        min_val = self.clamp_gui.getBottomValue();
        
        if not max_val < min_val: # Clamp only when possible
            if   val < min_val: val = min_val
            elif val > max_val: val = max_val
        
        return val
        
    def getTypeName(self):
        return "Simplex noise layer."
    
    def getTypeDescription(self):
      return "Layer whose values are generated using simplex noise algorithm."
    
    def copy(self, name):
        layer = SimplexLayer(name, self)
        return layer        
        
        
