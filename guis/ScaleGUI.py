from array2d import *

from random  import *
from Tkinter import *

   
# A simple gui that displays a scale.
class ScaleGUI():
    def __init__(self, label="Value", min_val=0, max_val=100):
        self.label = label
        self.value = IntVar()
        self.value.set(min_val)
        self.min = min_val
        self.max = max_val
        
    def layoutGUI(self, parent, heightmap):
        frame = LabelFrame(parent, text=self.label)
        frame.pack()
        
        self.value_slider = Scale(frame, label=self.label, 
            orient=HORIZONTAL, variable=self.value, from_=self.min, to=self.max
        )
        self.value_slider.pack()
        
    def getValue(self):
        return self.value.get()
        
    
    
