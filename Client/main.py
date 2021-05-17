import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk 
from view import app_viev

if __name__ == '__main__':
    window = app_viev()
    window.connect("delete-event", Gtk.main_quit)
    window.first_page.return_start_page()
    window.show()
    Gtk.main()