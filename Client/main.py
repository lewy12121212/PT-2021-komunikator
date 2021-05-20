import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk 
from view import App_view
from client import Client 



if __name__ == '__main__':
    #c = Client()
    window = App_view()
    window.connect("delete-event", Gtk.main_quit)
    window.chat_window.return_start_page()
    window.show()
    Gtk.main()