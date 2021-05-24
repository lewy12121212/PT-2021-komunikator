import gi
import atexit
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk 
#Łukasz
#from view import App_view
#from client import Client 

#Łukasz
from view_kopia import App_view 


if __name__ == '__main__':
    #c = Client()
   
    window = App_view()
    window.connect("delete-event", window.on_destroy)
    #Łukasz
    #window.chat_window.return_start_page()
    window.login_window.Show_login_window()
    window.show()
    Gtk.main()

    