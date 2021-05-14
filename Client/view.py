import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk
from gi.repository.GdkPixbuf import Pixbuf

class app_view(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Komunikator")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)
        pom = Gtk.Grid(row_spacing = 5)
        self.add(pom)
        pom.add(self.contact_tabel())
        pom.attach(self.contact_list(), 0, 1, 1, 1)
        #pom.attach_next_to(self.contact_tabel(), self.contact_list(), Gtk.PositionType.BOTTOM, 1, 2)
       
        
    def contact_tabel(self):
          
        # Create Box
        hbox = Gtk.Box(spacing = 10)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, 
                    spacing = 10)
        vbox_left.set_homogeneous(False)
       
   
        hbox.pack_start(vbox_left, True, True, 0)
        
          
        # Create label
        label = Gtk.Label("Kontakty")
        vbox_left.pack_start(label, True, True, 0)
        self.add(hbox)
        return hbox
        
        
    def contact_list(self):
        grid = Gtk.Grid()
        self.add(grid)
        
        buttons = [] 
        
        for user in global_functions.active_user_list:
            buttons.append(Gtk.Button(label=user))

        grid.add(buttons[0])
        for previous_button, button in zip(buttons,buttons[1:]):
            grid.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 2)

        return grid
        '''grid.attach_next_to(button2, button1, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(button3, button2, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(button4, button3, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(button5, button4, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(button6, button5, Gtk.PositionType.BOTTOM, 1, 2)
        '''
