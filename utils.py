import random

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



# Seeding functions:
randomizer = random.Random()
seeding_states = {}
def setSeedNumber(new_seed):
  global seeding_states
  
  print(new_seed)
  
  if new_seed in seeding_states:
    state = seeding_states[new_seed]
    randomizer.seed(new_seed)
    randomizer.setstate(state)
    print("retreiving seed")
  else:
    randomizer.seed(new_seed)
    state = randomizer.getstate()
    seeding_states[new_seed] = state
    print("new seed")
  

def getNextSeedInt(low, high):
  return randomizer.randint(low, high)
  



if __name__ == "__main__":
  setSeedNumber(0)
  n = getNextSeedInt(0,10)
  print(n)
  n = getNextSeedInt(0,10)
  print(n)
  n = getNextSeedInt(0,10)
  print(n)
  
  print("----------------")
  
  setSeedNumber(100)
  n = getNextSeedInt(0,10)
  print(n)
  n = getNextSeedInt(0,10)
  print(n)
  n = getNextSeedInt(0,10)
  print(n)

  print("----------------")
  setSeedNumber(0)
  n = getNextSeedInt(0,10)
  print(n)
  n = getNextSeedInt(0,10)
  print(n)
  n = getNextSeedInt(0,10)
  print(n)

  
  
  
  
  
  
  
