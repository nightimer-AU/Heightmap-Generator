
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
  def apply(self, layer_val, cumulative_val):
    return layer_val + cumulative_val

  def getName(self):
    return "Add"
    
  