from layers import *

from tkMessageBox import *
from Tkinter import *
from PIL import Image, ImageTk


# The heigtmap generator main entry point class.
class HeightmapGenerator:
  def __init__(self):
    
    root = Tk()
    
    self.heightmap = None # Current heightmap. 
    self.layers_factory = LayersFactory()
    self.layers = {}
    
    self.root = root
    root["padx"] = 10
    root["pady"] = 4
    root.geometry("800x600")
    
    menu = Menu(root)
    self.menu = menu
    root.config(menu=menu)
    
    file_menu = Menu(menu)
    menu.add_cascade(menu=file_menu, label="File")
    
    file_menu.add_command(label="New", command=self.newHeightmap)
  
   
    self.left = Frame(root)
    self.left.pack(side=LEFT, fill=BOTH)
   
    self.right = Frame(root)
    self.right.pack(side=LEFT)
   
    self.createLayersPane()
    self.createLayersSettings()
    self.createActionButtons()
    self.createCanvas()
    
    
 
  def createLayersPane(self):
    # Create the layers-pane frame:
    layers = LabelFrame(self.left, text="Layers")
    layers.pack(fill=Y)
    
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
    layer_list.bind("<Double-Button-1>", self.displayLayerSettings)
    layer_list.pack()
    layer_list.insert(0, "First")
    
    ## Create layers moving buttons:
    ### First the frame that will make them align horizontal:
    up_down_frame = Frame(layers)
    up_down_frame.pack(fill=X)
    
    up_button = Button(up_down_frame, text="/\\")
    up_button["command"] = self.moveLayerUp
    up_button.pack(side=LEFT, expand=YES)
    
    down_button = Button(up_down_frame, text="\\/")
    down_button["command"] = self.moveLayerDown
    down_button.pack(side=LEFT, expand=YES)
    
    
    
  def createLayersSettings(self):
    layer_settings = LabelFrame(self.left, text = "Layer settings")
    self.layer_settings = layer_settings
    self.ls_container = Frame(layer_settings)
    self.ls_container.pack()
    layer_settings.pack(expand=YES, fill=BOTH)
    
  def createActionButtons(self):
    actions = LabelFrame(self.left, text="Actions")
    actions.pack(fill=X)
    generate = Button(actions, text="GENERATE")
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
      
  def displayLayerSettings(self, event):
    self.ls_container.pack_forget()
    self.ls_container.destroy()
    ls_container = Frame(self.layer_settings)
    self.ls_container = ls_container
    ls_container.pack()
    
    idx = self.layer_list.curselection()[0]
    layer_name = self.layer_list.get(idx)
    layer = self.layers[layer_name]
    
    layer.layoutGUI(ls_container)

      
  def moveLayerDown(self):
    idx_old = self.layer_list.curselection()[0]
    idx_new = idx_old + 1
    
    # Check if we would go out of the bounds of the list:
    if idx_new > self.layer_list.size() - 1: return
    
    val = self.layer_list.get(idx_old)
    self.layer_list.delete(idx_old)
    self.layer_list.insert(idx_new, val)
    self.layer_list.selection_set(idx_new)
    
  def moveLayerUp(self):
    idx_old = self.layer_list.curselection()[0]
    idx_new = idx_old - 1

    # Check if we would go out of the bounds of the list:
    if idx_new < 0: return
    
    val = self.layer_list.get(idx_old)
    self.layer_list.delete(idx_old)
    self.layer_list.insert(idx_new, val)
    self.layer_list.selection_set(idx_new)
    
  
      
  def delLayer(self):
    idx = self.layer_list.curselection()[0]
    self.layer_list.delete(idx)
  
  def start(self):
    self.root.mainloop()


class Dialog():
  def __init__(self, parent, title):
    win = Toplevel(parent)
    self.win = win
    win.title(title)
    win["padx"] = 10
    win["pady"] = 10
  
    self.createControls()
  
    win.protocol("WM_DELETE_WINDOW", self.destroy)
    win.focus_set()
    win.grab_set()
    parent.wait_window(win)
  
  def createControls(self):
    pass

  def destroy(self):
    self.win.destroy()

class TextDialog(Dialog):
  def __init__(self, parent, title, message, value):
    self.message = message
    self.value   = value
    self.OK = False
    Dialog.__init__(self, parent, title)

  def createControls(self):
    entry_frame = Frame(self.win)
    entry_frame.pack()
    
    label = Label(entry_frame, text=self.message)
    label.pack()
    entry = Entry(entry_frame, text=self.value)
    self.entry = entry
    entry.pack()
    
    buttons_frame = Frame(self.win)
    buttons_frame.pack()
    
    ok_button = Button(buttons_frame, text="OK")
    ok_button["command"] = self.ok
    ok_button.pack(side=LEFT)
    
    cancel_button = Button(buttons_frame, text="CANCEL")
    cancel_button["command"] = self.destroy
    cancel_button.pack(side=LEFT)
    
    
  def ok(self):
    self.value = self.entry.get()
    self.OK = True
    self.win.destroy()
    
  def getValue(self):
    return self.value
    

class NewLayerDialog(Dialog):
  def __init__(self, parent, layers_factory):
    self.OK = False
    self.layers_factory = layers_factory
    self.new_layer = None # The new layer that will be created.
    Dialog.__init__(self, parent, "New layer")
  
  def createControls(self):
    # The top frame: 
    tf = Frame(self.win)
    tf.pack()
    
    ## The name entry:
    nl = Label(tf, text="Layer name:")
    nl.grid(row=0, column=0)
    ne = Entry(tf)
    self.name_entry = ne
    ne.grid(row=0, column=1)
    
    
    # The middle frame
    bf = Frame(self.win)
    self.middle_frame = bf
    bf.pack(fill=X)

    ## The type radiobuttons
    self.type_idx = IntVar()
    protos = self.layers_factory.getPrototypes()
    for proto_idx in range(0, len(protos)):
      proto = protos[proto_idx]
      self.createTypeRadioButton(proto_idx, proto.getTypeName())
    
    ## The type description text widget:
    type_desc = Message(bf, 
      text="Please select layer type using the radio buttons above.\
            The description of the selected type will display here.")
    self.type_desc = type_desc
    type_desc["borderwidth"] = 2
    type_desc["relief"] = SOLID
    type_desc["background"] = "white"
    type_desc.pack(fill=X)
    
    
    # The bottom frame (with OK and CANCEL buttons):
    bbf = Frame(self.win)
    bottom_frame = bbf
    bbf.pack()
    ok_button = Button(bbf, text="OK")
    ok_button["command"] = self.ok
    ok_button.pack(side=LEFT)
    cancel_button = Button(bbf, text="Cancel")
    cancel_button["command"] = self.destroy
    cancel_button.pack(side=LEFT)
    
  def createTypeRadioButton(self, idx, type_name):
    radio = Radiobutton(self.middle_frame, value=idx, text=type_name)
    radio["command"] = self.typeChanged
    radio.pack()
  
  def typeChanged(self):
    idx = self.type_idx.get()
    protos = self.layers_factory.getPrototypes()
    proto = protos[idx]
    self.type_desc["text"] = proto.getTypeDescription()
    
  def ok(self):
    idx = self.type_idx.get()
    protos = self.layers_factory.getPrototypes()
    proto = protos[idx]
    name = self.name_entry.get()
    self.new_layer = proto.copy(0, name)
    self.OK = True
    self.destroy()
    
  def getNewLayer(self):
    return self.new_layer


# Dialog displayed when a new heightmap is created.
class HeightmapDialog(Dialog):
  def __init__(self, parent):
    Dialog.__init__(self, parent, "New heightmap")
    
  def createControls(self):
    self.width  = 0
    self.height = 0
    
    # Width label and entry:
    w_label = Label(self.win, text="Width:")
    w_label.grid(row=0, column=0)      
    w_entry = Entry(self.win)
    w_entry.grid(row=0, column=1)
    self.w_entry = w_entry
    # Height label and entry:
    h_label = Label(self.win, text="Height:")
    h_label.grid(row=1, column=0)
    h_entry = Entry(self.win)
    h_entry.grid(row=1, column=1)
    self.h_entry = h_entry
    
    # Ok button.  
    ok_button = Button(self.win, text="OK")
    ok_button["command"] = self.ok
    ok_button.grid(columnspan=2)
    
    
  def ok(self):
    is_error = False
    try:
      self.width  = int(self.w_entry.get())
      self.height = int(self.h_entry.get())
    except ValueError as e:
      is_error = True
  
    if(self.width < 1) or (self.height < 1):
      is_error = True
  
    if is_error:
      showerror(
        "Invalid values", 
        "The supported width and height values must be positive, \
         non-zero integral values.")
      return
    else:
      self.destroy()

images = {}    
def loadImage(path):
  img = Image.open(path)
  tk_img = ImageTk.PhotoImage(img)
  images[path] = tk_img # Just keeping the reference to avoid GC (see ImageTk docs)
  return tk_img
    
if __name__ == "__main__":
  app = HeightmapGenerator()
  app.start()
