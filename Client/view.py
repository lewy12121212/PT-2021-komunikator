import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk
from gi.repository.GdkPixbuf import Pixbuf
import sys
#import client


class app_view(Gtk.Window):
    ##Do wyglądądu podłączyć css 
    def __init__(self):
        Gtk.Window.__init__(self, title="Komunikator")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)
        self.set_default_size(800,400)

        self.login()
        #self.registration()
        #self.main_chat_window()
        #self.contact_change()

    def main_chat_window(self):
        #pom to okno główne
        pom = Gtk.Grid(row_spacing = 5,column_spacing = 10)
        self.add(pom)

        #contacts zawiera rzeczy związane z listą kontaktów
        contacts = Gtk.Grid(row_spacing = 5)
        self.add(contacts)
        contacts.add(self.contact_tabel())
        contacts.attach(self.contact_buttons(), 0, 1, 1, 1)
        contacts.attach(self.contact_list(), 0, 2, 1, 2)

        #Okno czatu 
        chat_window = Gtk.Grid(row_spacing = 5)
        self.add(chat_window)
        chat_window.attach(self.entry_to_send(), 1, 2, 1, 1)
        chat_window.attach(self.messages(), 1,0, 1, 1)

        profile = Gtk.Grid(row_spacing = 5)
        self.add(profile)
        profile.add(self.profile_buttons())

        pom.add(contacts)
        pom.attach(chat_window, 1, 0, 1, 1)
        pom.attach(profile, 1, 1, 1, 1)

    def contact_change(self):
        vboxa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.add(vboxa)
        vboxa.set_hexpand(True)
        label = Gtk.Label("Podaj nazwę użytkownika: ")
        vboxa.pack_start(label, True, True, 0)

        #Okno do wpisywania tekstu
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        vboxa.pack_start(self.entry, True, True, 0)
         

    def profile_buttons(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(vbox)
        self.send_button = Gtk.Button(label="Zmiana hasła")
        vbox.pack_start(self.send_button, True, True, 0)
        self.send_button = Gtk.Button(label="Usuń konto")
        vbox.pack_start(self.send_button, True, True, 0)
    
        return vbox    

    def contact_buttons(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(vbox)
        self.send_button = Gtk.Button(label="Dodaj kontakt")
        vbox.pack_start(self.send_button, True, True, 0)
        self.send_button = Gtk.Button(label="Usuń kontakt")
        vbox.pack_start(self.send_button, True, True, 0)
    
        return vbox

    def login(self):
        login = Gtk.Grid(row_spacing = 10,column_spacing = 10)
        self.add(login)
        
        login.add(self.login_label())
        login.attach(self.login_entry(), 0, 1, 1, 1)
        login.attach(self.password_entry(), 0, Gtk.PositionType.BOTTOM, 1, 2)
        login.attach(self.login_button("Zaloguj"), 1, 1, 1, 1)


    def login_button(self,name):
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(vbox)
        self.send_button = Gtk.Button(label=name)
        self.send_button.connect("clicked", self.on_login_click)
        vbox.pack_start(self.send_button, False, False, 0)

        return vbox

    def on_login_click(self, button):
        print("zaloguj")


    def registration(self):
        login = Gtk.Grid(row_spacing = 10,column_spacing = 10)
        self.add(login)
        
        login.add(self.login_label())
        login.attach(self.login_entry(), 0, 1, 1, 1)
        login.attach(self.password_entry(), 0, Gtk.PositionType.BOTTOM, 1, 2)   
        login.attach(self.login_button("Zarejestruj"), 1, 1, 1, 1) 

    def password_entry(self):
        vboxa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.add(vboxa)
        vboxa.set_hexpand(False)
        label = Gtk.Label("Hasło: ")
        #label.set_alignment(0.5,0)
        vboxa.pack_start(label, False, False, 20)

        #Okno do wpisywania tekstu
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        #self.entry.set_alignment(0)
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        vboxa.pack_start(self.entry, False, False, 1) 
        return vboxa   

    def login_entry(self):
        vboxa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.add(vboxa)
        vboxa.set_hexpand(False)
        label = Gtk.Label("Login: ")
        #label.set_alignment(0.5,0)
        vboxa.pack_start(label, False, False, 20)

        #Okno do wpisywania tekstu
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        #self.entry.set_alignment(0)
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        vboxa.pack_start(self.entry, False, False, 1) 

        return vboxa   

    def login_label(self):
       
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
    
        label = Gtk.Label("Logowanie")
        label.set_hexpand(True)
        #label.set_alignment(1,0)
        vbox.pack_start(label, True, True, 0)
        self.add(vbox)
        return vbox


       

    def messages(self):
        hbox = Gtk.Box(spacing = 10)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        vbox_left.set_homogeneous(False)
        hbox.pack_start(vbox_left, True, True, 0)
       
        '''
        #Wiadomość - podzielić na tablicę wiadomości
        label = Gtk.Label("Jakas wiadomoscqwert yuiolk wertyui dfghj sdfghj sdfghjk ertyui sdfghjkl sdfghjk ertyui dfghj sdfghj ertyui zxcvbnm sdfghj ertyui dfghj jhgfdsazxcvbnm, qwea f fdsfgdf asfddSADASDA dd rtyui hgfdsdfgh bvcdsd rftgyhjmnbvfdertyhgfrtghbvf rtgb fvrtgbvcdfg h")
        label.set_max_width_chars(32)
        label.set_line_wrap(True)
        label.set_alignment(0,0)
        vbox_left.pack_start(label, True, True, 0)
        '''
        #Okno do scrolowania
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_size_request(600,200)
        scrolled_window.set_max_content_width(50) 
        scrolled_window.set_border_width(10) ##Odstęp po prawej

        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        messages = []
        for message in global_functions.income_messages_list:
            messages.append(message)
            
        for message in messages:
            if(message[1]==1):
                label = Gtk.Label(message[0])
                label.set_line_wrap(True)
                label.set_max_width_chars(5)
                label.set_alignment(0,0)
                vbox_left.pack_start(label, True, False, 1)
            else:
                label = Gtk.Label(message[0])
                label.set_line_wrap(True)
                label.set_max_width_chars(5)
                label.set_alignment(1,0)
                vbox_left.pack_start(label, True, False, 1)

        #Dodanie do okna scrolowania wiadomości
        scrolled_window.add_with_viewport(hbox)
        
        # add the scrolledwindow to the window
        self.add(scrolled_window)   

        #self.add(hbox)
        return scrolled_window  


    #Wysyłanie wiadomości
    def entry_to_send(self):
        #Zawiera pole do wpisywania i guzik do wysyłania
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(vbox)

        #Okno do wpisywania tekstu
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        vbox.pack_start(self.entry, True, True, 0)

        #Przycisk do wysyłania tekstu
        self.send_button = Gtk.Button(label="Wyślij")
        vbox.pack_start(self.send_button, True, True, 0)

    
        return vbox

    #Etykieta listy kontaktów
    def contact_tabel(self):
          
        hbox = Gtk.Box(spacing = 10)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        vbox_left.set_homogeneous(False)
        hbox.pack_start(vbox_left, True, True, 0)
  
        label = Gtk.Label("Kontakty")
        vbox_left.pack_start(label, True, True, 0)
        self.add(hbox)
        return hbox
        
    #Lista kontaktów
    def contact_list(self):
        grid = Gtk.Grid()
        self.add(grid)
        
        buttons = [] 
        
        #Dla każdego kontaktu z listy tworzy podpisany przycisk
        for user in global_functions.active_user_list:
            buttons.append(Gtk.Button(label=user))

        grid.add(buttons[0])
        for previous_button, button in zip(buttons,buttons[1:]):
            grid.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 2)
        
        return grid
