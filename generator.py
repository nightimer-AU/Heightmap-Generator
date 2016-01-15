from layers    import *
from dialogs   import *
from utils     import *
from heightmap import *

from tkMessageBox import *
from Tkinter      import *



# The heigtmap generator main entry point class.
class HeightmapGenerator:
  def __init__(self):
    
    root = Tk()
    self.root = root
    root.title("Heightmap generator")
    root.tk.call('wm', 'iconphoto', root._w, loadImage("app.ico"))  
        
    
    self.heightmap = Heightmap(10,10) # Current heightmap. 
    self.layers_factory = LayersFactory() 
    self.layers = {} # A dictionary mapping from layer name to a layer
    self.current_layer = DummyLayer()
    
    root["padx"] = 10
    root["pady"] = 4
    root.geometry("800x600+0+0")
    
    menu = Menu(root)
    self.menu = menu
    root.config(menu=menu)
    
    file_menu = Menu(menu)
    menu.add_cascade(menu=file_menu, label="File")
    
    file_menu.add_command(label="New", command=self.newHeightmap)
  
    # Create left panel:
    self.left = Frame(root)
    self.left.pack(side=LEFT, fill=BOTH)
   
    # Create right panel:
    self.right = Frame(root)
    self.right.pack(side=LEFT)
   
    self.createHeightmapPane()
    self.createLayersPane()
    self.createLayersSettings()
    self.createActionButtons()
    self.createCanvas()
    
    
  def createHeightmapPane(self):
    hm_frame = LabelFrame(self.left, text="Heightmap")
    hm_frame.pack(fill=X)

    hm_width  = self.heightmap.getWidth()
    hm_height = self.heightmap.getHeight()
    dims_txt = "W:%d H:%d" % (hm_width, hm_height)
    self.hm_dims = Label(hm_frame, text=dims_txt )
    self.hm_dims.pack()
 
  def createLayersPane(self):
    # Create the layers-pane frame:
    layers = LabelFrame(self.left, text="Layers")
    layers.pack(fill=BOTH)
    
    ## Create layer buttons:
    new_layer = Button(layers, text="New layer")
    new_layer["command"] = self.newLayer
    new_layer.pack(fill=X)
    
    del_layer = Button(layers, text="Delete layer")
    del_layer["command"] = self.delLayer
    del_layer.pack(fill=X)
    
    
    ## Create the layers list:
    layer_list = Listbox(layers, selectmode=SINGLE)
    self.layer_list = layer_list
    layer_list.bind("<Double-Button-1>", self.changeCurrentLayer)
    layer_list.pack()
   
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
    
    
    
  def createLayersSettings(self):
    layer_settings = LabelFrame(self.left, text = "Layer settings")
    self.layer_settings = layer_settings
    layer_settings.pack(expand=YES, fill=BOTH)
    
    # Layer mode frame:
    lm_frame = Frame(layer_settings)
    lm_frame.pack()
    
    lm_label = Label(lm_frame, text="Layer mode:")
    lm_label.pack(side=LEFT)
    
    self.layer_mode = StringVar(layer_settings)
    self.layer_mode.set("Add")
    lm_combo = OptionMenu(lm_frame, self.layer_mode,
      "Add", "Subtract", "Multiply", "Divide", "Mix", "Dissolve",
      command=self.setLayerMode
      )
    lm_combo.pack(side=LEFT)
    
    self.ls_container = Frame(layer_settings)
    self.ls_container.pack()
    
  def createActionButtons(self):
    actions = LabelFrame(self.left, text="Actions")
    actions.pack(fill=X)
    generate = Button(actions ,
      text="Generate heightmap", image=loadImage("generate.png"), 
      compound=LEFT)
    generate["command"] = self.generateHeightmap
    generate.pack()

  def createCanvas(self):
    # Create the right-pane frame:
    right = LabelFrame(self.root, text="Preview")
    right.pack(side=LEFT, fill=BOTH, expand=YES)
    # Create the preview canvas:
    canvas = Canvas(right)
    self.canvas = canvas
    canvas["width"] = 500
    canvas["height"] = 500
    canvas["background"] = "black"
    canvas.pack(anchor=CENTER, expand=YES)
    
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
    # Read the selection before we lose focus in the dialog
    if len(selection) == 1:
      idx = selection[0]
    else: idx = 0
    dialog = NewLayerDialog(self.root, self.layers_factory)
    # Here the list box lost focus, so I need to restore it afterwards the text was entered.
    if dialog.OK:
      new = dialog.getNewLayer()
      self.layer_list.insert(idx, new.name)
      self.layer_list.selection_set(idx) # Restoring the selection
      self.layers[new.name] = new
      
  # Change the current layer the user is working on.
  # Fired by a double button press on the layers listbox.
  def changeCurrentLayer(self, event):
    idx = self.layer_list.curselection()[0]
    layer_name = self.layer_list.get(idx)
    layer = self.layers[layer_name]
    self.current_layer = layer
    
    self.readLayerMode()
    self.displayLayerSettings()

  def readLayerMode(self):
    l_mode = self.current_layer.getMode()
    mode_name = l_mode.getName()
    
    self.layer_mode.set(mode_name)
    
  def setLayerMode(self, idx):
    new_name = self.layer_mode.get()
    new_mode = LayerMode.fromName(new_name)
    
    self.current_layer.setMode(new_mode)
    
  def displayLayerSettings(self):
    self.ls_container.pack_forget()
    self.ls_container.destroy()

    ls_container = Frame(self.layer_settings)
    self.ls_container = ls_container
    ls_container.pack(fill=X)
    
    self.current_layer.layoutGUI(ls_container)

      
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
      showwarning("No layers!", "Cannot generate heightmap - no layers defined.")
      return
    
    # Create the layers stack:
    stack = LayerStack()
    for idx in range(0, n_layers):
      l_name = l_list[idx]
      layer = self.layers[l_name]
      layer.setIndex(idx)
      stack.append(layer)
    
    layer = stack.get(0)
    print("layer??? ", str(layer))
    cumulative = self.heightmap.getInitialHeights()
    
    print("Generating:")
    while layer != None:
      print("layer:")
      print(layer.getTypeName())
      layer.apply(stack, cumulative)
      layer = layer.getNext(stack)
    
    print("Cumulative:")
    print(str(cumulative))
    
      

if __name__ == "__main__":
  app = HeightmapGenerator()
  app.start()
