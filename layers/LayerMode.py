
########################################
# All the modes for the layer operation.
########################################

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


