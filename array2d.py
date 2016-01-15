from __future__ import division
from random import *
from math   import *
# Heightmap generator. A prototype.

class Interpolator():
  
  def interpolate(self, v1, v2, t):
    t = self.clampT(t)
    return self.doInterpolation(v1, v2, t)

  def doInterpolation(self, v1, v2, t):
    pass # Abstract method

  def clampT(self, t):
    if t < 0: return 0
    if t > 1: return 1
    else:     return t

class lerp(Interpolator):
  def doInterpolation(self, v1, v2, t):
    return \
      v1 * (1 - t ) + \
      v2 * (0 + t )

class slerp(Interpolator):
  def doInterpolation(self, v1, v2, t):
    d = (sin(t * pi - pi /2) / 2) + 0.5
    print(d)
    val = v1 * (1 - d) + v2 * d
    return val

class Array2D():
  # Constructor.
  # It sets the initial values of the 2d array to zeros.  
  # w, h - ints - the width and heigh of the heightmap
  def __init__(self, w , h): 
    self.width = w
    self.height = h
    self.values = []
    for x in range(0, w):
      self.values.append([])
      for y in range(0, h):
        self.values[x].append(0)
        
  def getWidth(self):
    return self.width
    

  def getHeight(self):
    return self.height

  def set(self, x, y, value):
    x = self.clampX(x)
    y = self.clampY(y)
    self.values[x][y] = value

  def get(self, x, y):
    x = self.clampX(x)
    y = self.clampY(y)
    return self.values[x][y]

  def clampX(self, x):
    if x < 0: return 0
    elif x >= self.width: return self.width - 1
    else: return x

  def clampY(self, y):
    if y < 0: return 0
    elif y >= self.height: return self.height - 1
    else: return y

  def printSelf(self):
    print(self)
  
  def each(self, callback):
    for y in range(0, self.height):
      for x in range(0,self.width):
        orig = self.get(x,y)
        new  = callback(x, y, orig)
        self.set(x, y, new)

  def __str__(self):
    astr = ""
    for y in range(0, self.height):
      for x in range(0, self.width):
        astr += str(self.get(x,y)) + " "
      astr += "\n"
    return astr

  def makeInterpolated(self, target_w, target_h, ipl):

    ratio_x = (self.width - 1) / (target_w - 1)
    ratio_y = (self.height- 1) / (target_h - 1)    

    other = Array2D(target_w, target_h)    

    for y_other in range(0, target_h):
      for x_other in range(0, target_w):
        x_real = ratio_x * x_other
        y_real = ratio_y * y_other
        x_lo = int(x_real)
        x_hi = int(x_real) + 1
        y_lo = int(y_real) 
        y_hi = int(y_real) + 1
      
        try:
          t_hor = (x_real - x_lo) / (x_hi - x_lo)
        except:
          t_hor = 0

        val_h1 = self.get(x_lo, y_lo)
        val_h2 = self.get(x_hi, y_lo)
        val_v1 = ipl.interpolate(val_h1, val_h2, t_hor)   

        val_h3 = self.get(x_lo, y_hi)
        val_h4 = self.get(x_hi, y_hi)
        val_v2 = ipl.interpolate(val_h3, val_h4, t_hor)
        
        try:
          t_ver = (y_real - y_lo) / (y_hi - y_lo)   
        except:
          t_ver = 0

        val_result = ipl.interpolate(val_v1, val_v2, t_ver)  
        
        other.set(x_other, y_other, val_result)

    return other


def printSep(name):
  print("**************** " + name + " ****************" )
  print("")

def test0():
  printSep("TEST 0")
  ipl = lerp()
  val = ipl.interpolate(0, 2, 0.75)
  #print(val)
  
  ipl = slerp()
  val = ipl.interpolate(0 ,10, 0)
  val = ipl.interpolate(0 ,10, 0.5)
  val = ipl.interpolate(0 ,10, 1)
  #print(val)


def test1():
  printSep("TEST 1")
  a2d = Array2D(3,3)

  def randomized(x, y, orig):
    delta = uniform(-10,10)
    return orig + delta

  a2d.each(randomized)
  print(a2d)

def test2():
  printSep("TEST 2")  
  a2d = Array2D(2,2)

  a2d.set(0,0, 0)
  a2d.set(1,0, 1)
  a2d.set(0,1, 1)
  a2d.set(1,1, 2)
  
  iptd = a2d.makeInterpolated(3,3, lerp())
  
  print(iptd)

if __name__ == "__main__":
  test0()
  test1()
  test2()  
  


