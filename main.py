import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk 
from view import app_view

win = app_view()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()