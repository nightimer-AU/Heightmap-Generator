from Tkinter import *
from PIL import Image, ImageTk

# Utility functions and classess.

# Image loader functions
images = {}    
def loadImage(name):
  img = Image.open("images/" + name)
  tk_img = ImageTk.PhotoImage(img)
  images[name] = tk_img # Just keeping the reference to avoid GC (see ImageTk docs)
  return tk_img
    
