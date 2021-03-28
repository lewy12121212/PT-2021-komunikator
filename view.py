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
        #self.send_msg_box()
        self.main_grid()

#msg bar
    def send_msg_container(self):
        # msg content
        msg_contents = Gtk.Entry()

        # button to send MSG
        send_button = Gtk.Button(label="SEND")
        
        send_button.connect("clicked", gui_callbacks.on_send_button_clicked)

        #box for send msg bar
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(user_box)
        user_box.pack_start(msg_contents, True, True, 0)
        user_box.pack_start(send_button, True, True, 0)

        return user_box

#active user list
    def users_list(self):

        #avatar static img
        self.avatar_img = Gtk.Image()
        self.avatar_img.set_from_file("./img/user.png")

        #create listbox
        self.users_listbox = Gtk.ListBox()
        framed_users_list = Gtk.Frame()
        framed_users_list.add(self.users_listbox)

        #iterate in list of active user
        for user in self.get_active_users():
            self.users_listbox.add(user)

        return framed_users_list

    def get_active_users(self):
        users: users_list = global_functions.active_user_list
        return[self.get_user_box(elem) for elem in users]

    def get_user_box(self, elem):
        row = Gtk.ListBoxRow()
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #user_box.pack_start(self.avatar_img, True, True, 0)
        user_box.pack_start(Gtk.Label(label=elem), True, True, 0)
        #box.connect("clicked", gui_callbacks.channel_callback)
        row.add(user_box)
        return row

#frame of conversation
    def conversation_frame():
        conversation = Gtk.Frame() #pole konwersacji
        #conversation.add()
        return conversation

#main interface function
    def main_grid(self):
        grid = Gtk.Grid()
        self.add(grid)

        #add elements of interface
        user_box = self.send_msg_container()
        framed_users_list = self.users_list()
        #conversation_frame = self.conversation_frame()

        #arrangement of elements
        grid.add(user_box)
        #grid.attach(self.send_button, 10, 0, 2, 1)
        grid.attach_next_to(framed_users_list, user_box, Gtk.PositionType.LEFT, 40, 20)
        #grid.attach_next_to(conversation_frame, framed_users_list, Gtk.PositionType.RIGHT, 1,2)
        

    