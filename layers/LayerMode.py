########################################
# All the modes for the layer operation.
########################################

# Layer mode represents operation that is done on the 
# the cumulative values of the current layer application.
class LayerMode():

    def __init__(self, name):
        self.name = name

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
        if name == "Mix":      new_mode = MixLayerModel()
        if name == "ColorDodge": new_mode = ColorDodgeLayerMode()
        if name == "Screen": new_mode = ScreenLayerMode()
        return new_mode


class AddLayerMode(LayerMode):
    def __init__(self):
        LayerMode.__init__(self, "Add")

    def apply(self, cum_h, layer_h):
        return cum_h + layer_h

    def getName(self):
        return "Add"


class SubtractLayerMode(LayerMode):
    def __init__(self):
        LayerMode.__init__(self, "Subtract")

    def apply(self, cum_h, layer_h):
        return cum_h - layer_h

    def getName(self):
        return "Subtract"


class MultiplyLayerMode(LayerMode):
    def __init__(self):
        LayerMode.__init__(self, "Multiply")

    def apply(self, cum_h, layer_h):
        return cum_h * layer_h

    def getName(self):
        return "Multiply"


class DivideLayerMode(LayerMode):
    def __init__(self):
        LayerMode.__init__(self, "Divide")

    def apply(self, cum_h, layer_h):
        return cum_h / layer_h

    def getName(self):
        return "Divide"


class MixLayerModel(LayerMode):
    def __init__(self):
        LayerMode.__init__(self, "Mix")

    def apply(self, cum_h, layer_h):
        return (cum_h + layer_h) / 2

    def getName(self):
        return "Mix"


class ColorDodgeLayerMode(LayerMode):
    def __init__(self):
        LayerMode.__init__(self, "ColorDodge")

    def apply(self, cum_h, layer_h):
        return layer_h / (1 - cum_h)

    def getName(self):
        return "ColorDodge"


class ScreenLayerMode(LayerMode):
    def __init__(self):
        LayerMode.__init__(self, "Screen")

    def apply(self, cum_h, layer_h):
        return 1 - (1 - cum_h) * (1 - layer_h)

    def getName(self):
        return "Screen"
