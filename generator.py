from __future__ import division
from dialogs    import *
from utils      import *
from heightmap  import *

from time         import *
from tkMessageBox import *
from Tkinter      import *

from PIL import Image, ImageTk
import PIL

from layers.DummyLayer import *

# The heigtmap generator main entry point class.
class HeightmapGenerator:
  def __init__(self):
    
    # Initialization:
    ## Make the root window, so things will work correctly:
    ## (the Tkinter variables: "IntVar", "StringVar", require
    ## an existing Tk instance to be active)  
    root = Tk()
    self.root = root
    root.title("Heightmap generator")
    root.tk.call('wm', 'iconphoto', root._w, loadImage("app.ico"))  
    root["padx"] = 10
    root["pady"] = 4
    root.geometry("800x800+0+0")
    
    ## Some of the intance variables:
    self.heightmap = Heightmap(100,100) # Current heightmap. 
    self.layers_factory = LayersFactory() 
    self.layers = {} # A dictionary mapping from layer name to a layer
    self.current_layer = DummyLayer()


    # Creating the UI layout.
    ## Create the menu for root window:
    self.createWindowMenu()
      
    ## Create the top frame:
    top_frame = Frame(root)
    top_frame.pack(expand=YES, fill=BOTH)
  
    ## Create left panel:
    self.left = Frame(top_frame)
    self.left.pack(side=LEFT, fill=BOTH, padx=2)
    self.createHeightmapPane()
    self.createLayersPane()
    self.createActionButtons()

    ## Create the layer settings panel:   
    layer_settings = LabelFrame(top_frame, text = "Layer settings")
    self.layer_settings = layer_settings
    layer_settings.pack( fill=BOTH, side=LEFT, ipadx=5, ipady=5, padx=2)
    self.createLayersSettings()
   
    ## Create right panel:
    self.right = Frame(top_frame)
    self.right.pack(side=LEFT, fill=BOTH, expand=YES, padx=2)
    self.createCanvas()
    
    ## Create the status bar panel:
    status_frame = Frame(root)
    status_frame.pack(fill=BOTH)
    self.status = Label(status_frame, text="Status bar.")
    self.status.pack()
    
    ## Trigger the layer change event do display the dummy layer:
    self.changeCurrentLayer(None)

    
  def createWindowMenu(self):
    menu = Menu(self.root)
    self.menu = menu
    self.root.config(menu=menu)
    
    file_menu = Menu(menu)
    menu.add_cascade(menu=file_menu, label="File")
    
    file_menu.add_command(label="New", command=self.newHeightmap)
    
    file_menu.add_command(label="Exit", command=self.root.destroy)
    
  def createHeightmapPane(self):
    hm_frame = LabelFrame(self.left, text="Heightmap")
    hm_frame.pack(fill=X, ipadx=5, ipady=5)

    hm_width  = self.heightmap.getWidth()
    hm_height = self.heightmap.getHeight()
    dims_txt = "Width:%d Height:%d" % (hm_width, hm_height)
    self.hm_dims = Label(hm_frame, text=dims_txt )
    self.hm_dims.pack()
 
  def createLayersPane(self):
    # Create the layers-pane frame:
    layers = LabelFrame(self.left, text="Layers")
    layers.pack(fill=BOTH, expand=YES, ipadx=5, ipady=5)
    
    ## Create layer buttons:
    bw = 15 # Button width.
      
    new_layer = Button(layers, text="New layer")
    new_layer["width"]   = bw
    new_layer["command"] = self.newLayer
    new_layer.pack()
    
    del_layer = Button(layers, text="Delete layer")
    del_layer["width"]   = bw
    del_layer["command"] = self.delLayer
    del_layer.pack()
    
    dup_layer = Button(layers, text="Duplicate layer")
    dup_layer["command"] = self.duplicateLayer
    dup_layer["width"]   = bw
    dup_layer.pack()
    
    ## Create the layers list:
    layer_list = Listbox(layers, selectmode=SINGLE)
    self.layer_list = layer_list
    layer_list.bind("<Button-1>", self.changeCurrentLayer)
    layer_list.pack(expand=Y, fill=Y)
   
    ## Create layers moving buttons:
    ### First the frame that will make them align horizontal:
    up_down_frame = Frame(layers)
    up_down_frame.pack(fill=X)
    
    up_button = Button(up_down_frame, image=loadImage("layer_up.png"))
    up_button["command"] = self.moveLayerUp
    up_button.pack(side=LEFT, expand=YES)
    
    down_button = Button(up_down_frame, image=loadImage("layer_down.png"))
    down_button["command"] = self.moveLayerDown
    down_button.pack(side=LEFT, expand=YES)
    
  def createActionButtons(self):
    actions = LabelFrame(self.left, text="Actions")
    actions.pack(fill=X , ipadx=5, ipady=5)
    generate = Button(
      actions,
      text="Generate heightmap", image=loadImage("generate.png"), 
      compound=LEFT)
    generate["command"] = self.generateHeightmap
    generate.pack()
    
    
  def createLayersSettings(self):
    # Layer name frame:
    ln_frame = Frame(self.layer_settings)
    ln_frame.pack()
    
    ln_label = Label(ln_frame, text="Layer:")
    ln_label.pack(side=LEFT)

    ln_entry = Entry(ln_frame)
    self.layer_name_entry = ln_entry
    ln_entry.pack()
    
    # Layer mode frame:
    

    self.ls_container = Frame(self.layer_settings)
    self.ls_container.pack(expand=YES, fill=BOTH)
    

  def createCanvas(self):
    # Create the right-pane frame:
    prev = LabelFrame(self.right, text="Preview")
    prev.pack(side=LEFT, fill=BOTH, expand=YES)
    # Create the preview canvas:
    canvas = Canvas(prev)
    self.canvas = canvas
    canvas["width"] = 500
    canvas["height"] = 500
    canvas["background"] = "black"
    canvas.pack(anchor=CENTER, expand=YES)
    
    canvas.bind("<Motion>", self.displayHeight)
    
    img = loadImage("cliff.png")
    canvas.create_image(0,0, image=img)
  
  def newHeightmap(self):
    dialog = HeightmapDialog(self.root)
    width  = dialog.width
    height = dialog.height
    
    self.heightmap = Heightmap(width, height)
      
    self.hm_dims["text"] = "W:%d H:%d" % (width, height)
      
  def newLayer(self):
    selection = self.layer_list.curselection()
    n_selected = len(selection)
    if n_selected > 0:
      idx = selection[0] + 1 # For inserting after current layer.
    else: idx = 0
    default_name = "Layer %d" % self.layer_list.size()
    # Read the selection before we lose focus in the dialog
    dialog = NewLayerDialog(self.root, self.layers_factory, default_name)
    # Here the list box lost focus, so I need 
    # to restore it afterwards the text was entered.
    if dialog.OK:
      new = dialog.getNewLayer()
      self.insertLayer(new, idx)
      self.layer_list.selection_set(idx) # Restoring the selection
  
  def insertLayer(self, layer, position=END):
    layer_name = layer.getName()
    self.layer_list.insert(position, layer_name)
    self.layers[layer_name] = layer
      
  def duplicateLayer(self):
    selection = self.layer_list.curselection()
    n_selected = len(selection)
    if n_selected > 0:
      idx = selection[0]
    else: 
      showwarning("No layer selected to duplicate.")
      return
    
    layer_name = self.layer_list.get(idx)
    layer      = self.layers[layer_name]
    
    orig_name = layer.getName() # Original name
    new_name =  orig_name # New name (to be made)
    num = 2
    while new_name in self.layers:
      new_name = orig_name + str(num)
      num += 1

    
    dialog = TextDialog(self.root, 
      "Enter new name", "Please enter duplicated layer name", new_name
    )
    
    if dialog.OK:
      new_name = dialog.getValue()
      copied = layer.copy(new_name)
      self.insertLayer(copied, idx+1)
      
    
    
  
  # Change the current layer the user is working on.
  # Fired by a double button press on the layers listbox.
  def changeCurrentLayer(self, event):
    selection = self.layer_list.curselection()
    if len(selection) > 0:
      idx = selection[0]
      layer_name = self.layer_list.get(idx)
      layer = self.layers[layer_name]
      self.current_layer = layer
    
    self.readLayerName()
    
    self.updateLayerSettings()

  def readLayerName(self):
    new_name = self.current_layer.getName()
    self.layer_name_entry.delete(0,END)
    self.layer_name_entry.insert(INSERT, new_name)
    

  def setLayerMode(self, idx):
    new_name = self.layer_mode.get()
    new_mode = LayerMode.fromName(new_name)
    
    self.current_layer.setMode(new_mode)
    
  def updateLayerSettings(self):
    self.ls_container.pack_forget()
    self.ls_container.destroy()

    ls_container = Frame(self.layer_settings)
    self.ls_container = ls_container
    ls_container.pack(expand=YES, fill=BOTH)
    
    self.current_layer.layoutGUI(ls_container, self.heightmap)
      
  def moveLayerDown(self):
    selection =  self.layer_list.curselection()
    if len(selection) == 0: return
    idx_old = self.layer_list.curselection()[0]
    idx_new = idx_old + 1
    
    # Check if we would go out of the bounds of the list:
    if idx_new > self.layer_list.size() - 1: return
    
    val = self.layer_list.get(idx_old)
    self.layer_list.delete(idx_old)
    self.layer_list.insert(idx_new, val)
    self.layer_list.selection_set(idx_new)
    
  def moveLayerUp(self):
    selection =  self.layer_list.curselection()
    if len(selection) == 0: return
    idx_old = self.layer_list.curselection()[0]
    idx_new = idx_old - 1

    # Check if we would go out of the bounds of the list:
    if idx_new < 0: return
    
    val = self.layer_list.get(idx_old)
    self.layer_list.delete(idx_old)
    self.layer_list.insert(idx_new, val)
    self.layer_list.selection_set(idx_new)
      
  def delLayer(self):
    if not self.isLayerSelected(): return
    idx = self.layer_list.curselection()[0]
    self.layer_list.delete(idx)
  
  def start(self):
    self.root.mainloop()

  def isLayerSelected(self):
    sel = self.layer_list.curselection()
    if len(sel) == 0: return False
    else: return True
    
    
  def generateHeightmap(self):
    l_list = self.layer_list.get(0,END)
    n_layers = len(l_list)
    if(n_layers) == 0: 
      showwarning(
        "No layers!",
        "Cannot generate heightmap - no layers defined."
      )
      return
    
    
    self.setStatus("Generating heightmap...")
    
    # Create the layers stack:
    stack = LayerStack()
    for idx in range(0, n_layers):
      l_name = l_list[idx]
      layer = self.layers[l_name]
      layer.setIndex(idx)
      stack.append(layer)
    
    layer = stack.get(0)
    cumulative = self.heightmap.getInitialHeights()
    
    while layer != None:
      self.setStatus("Applying layer: \"%s\" ..." % layer.getName())
      layer.apply(stack, cumulative)
      layer = layer.getNext(stack)
    
    self.setStatus("Heightmap generated. Generating preview...")
    
    self.createPreview(cumulative)    
  
  
  # Create preview image and display it in preview area 
  def createPreview(self, cumulative):
    self.setStatus("Normalizing heightmap for image coloring...")

   
    
    w = self.heightmap.getWidth()
    h = self.heightmap.getHeight()
    image = PIL.Image.new("RGBA", (w,h))
    
    self.setStatus("Creating image preview...")
    
    for x in range(0, w):
      for y in range(0, h):
        height = int(cumulative.get(x,y))
        
        color = (height, height, height)
        image.putpixel((x,y), color)
        
    self.setStatus("Resizing the image to fit the preview bounds..,")
    image = image.resize(
      ( 1000, 1000 ), 
      PIL.Image.NEAREST
    )
      
    photo_img = ImageTk.PhotoImage(image)
    
    
    self.canvas.img = photo_img # Again keep that reference
    self.canvas.create_image(0,0, image=photo_img)
    
    self.setStatus("Done.")
    
  def displayHeight(self, event):
    pass
    
  def setStatus(self, txt):
    self.status["text"] = txt
    self.root.update()

if __name__ == "__main__":
  app = HeightmapGenerator()
  app.start()
