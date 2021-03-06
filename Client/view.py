from typing import Tuple
import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from client import Client
from response import Response
import sys
#import client

#https://stackoverflow.com/questions/46774286/change-window-frame-gtk3-pygtk-and-pass-parameters

c = Client()
resp = Response()




#Okno aplikacji
class App_view(Gtk.Window):
    def __init__(self):
       
        super(App_view, self).__init__(title="Komunikator")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)
        self.set_default_size(600, 250)

        container = Gtk.Grid()
        self.add(container)
        container.show()

        #Okno logowania
        self.login_window = Login_window(self)
        container.add(self.login_window)
        #Okno czatu
        self.chat_window = FirstPage(self)
        container.add(self.chat_window)
     
        


class Login_window(Gtk.Grid):
    #Konstruktor - wywołuje okno logowania
    def __init__(self, parent_window):
        super().__init__()
        self.__parent_window = parent_window
        self.row_spacing = 10
        self.column_spacing = 10
        self.login()

    #Chowa okno logowania i pokazuje okno czatu
    def swich_to_chat(self, *args):
        self.__parent_window.chat_window.show_all()
        self.hide()

 
    #Okno logowania
    def login(self):
        
        loog = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(loog)

        labela = Gtk.Label("Logowanie")

        obok = Gtk.Box(spacing=6)
        label_login = Gtk.Label("Login: ")
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(False)
        self.entry.set_vexpand(False)
        self.entry.set_text("admin")  

        obok2 = Gtk.Box(spacing=6)
        label_haslo = Gtk.Label("Hasło: ")
        self.entry2 = Gtk.Entry()
        self.entry2.set_hexpand(False)
        self.entry2.set_vexpand(False)
        self.entry2.set_text("admin")  
        
        obok.set_halign(3)
        obok.pack_start(label_login, True, True, 0)
        obok.pack_start(self.entry, True, True, 0)
        
     
        obok2.set_halign(3)
        obok2.pack_start(label_haslo, True, True, 0)
        obok2.pack_start(self.entry2, True, True, 0)

        labela.set_hexpand(True)
        loog.pack_start(labela, True, True, 0)
        loog.pack_start(obok, True, True, 0)
        loog.pack_start(obok2, True, True, 0)

        self.send_button = Gtk.Button(label="Zaloguj")
        self.send_button.connect("clicked", self.on_login_click)
        self.send_button.set_halign(3)
        self.send_button.set_hexpand(True)
        loog.pack_start(self.send_button, False, True, 0)
        

    def wrong_login(self):
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        label = Gtk.Label("Podano błędny login lub hasło")
        vbox.pack_start(label, True, True, 0)
        self.add(vbox)
        return vbox  


    def on_login_click(self, button):
        e = self.entry.get_text()
        o = self.entry2.get_text()

        mess = {"signal":"LOG", "data":{"login":e,"password":o}}
        
        c.send(str(mess))
        data = c.recv()
        print(data)
        if resp.Make_Response(data):
            c.login = e
            self.swich_to_chat()
        else:
            print(mess["data"])

        

    '''def registration(self):
        login = Gtk.Grid(row_spacing = 10,column_spacing = 10)
        self.add(login)
        
        login.add(self.login_label())
        login.attach(self.login_entry(), 0, 1, 1, 1)
        login.attach(self.password_entry(), 0, Gtk.PositionType.BOTTOM, 1, 2)   
        login.attach(self.login_button("Zarejestruj"), 1, 1, 1, 1) 
    '''


class FirstPage(Gtk.Grid):
    
    def __init__(self, parent_window):
       
        super().__init__()
        self.__parent_window = parent_window
        self.main_chat_window()
    

    def return_start_page(self, *args):
        self.__parent_window.login_window.show_all()
        self.hide()

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
         


    def main_chat_window(self):

        self.poziomo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.add(self.poziomo)

        self.kontakty = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.poziomo.pack_start(self.kontakty, False, True, 0)
        self.label_kontakty = Gtk.Label("Lista kontaktów")
        self.label_kontakty.set_valign(1)
        self.kontakty.pack_start(self.label_kontakty, False, True, 0)

        self.guziki_kontakty = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.dodaj_kontakt = Gtk.Button(label="Dodaj kontakt")
        self.guziki_kontakty.pack_start(self.dodaj_kontakt, True, True, 0)
        self.usun_kontakt = Gtk.Button(label="Usuń kontakt")
        self.guziki_kontakty.pack_start(self.usun_kontakt, True, True, 0)
        self.guziki_kontakty.set_valign(1)
        self.kontakty.pack_start(self.guziki_kontakty, False, True, 0)


      
        self.grid_contact = Gtk.Grid()
       
        
        self.buttons = [] 
        
        #Dla każdego kontaktu z listy tworzy podpisany przycisk
        for user in global_functions.active_user_list:
            self.buttons.append(Gtk.Button(label=user,xalign=0))

        self.grid_contact.add(self.buttons[0])
        for previous_button, button in zip(self.buttons,self.buttons[1:]):
            self.grid_contact.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
        
        self.scrolled_kontakty = Gtk.ScrolledWindow()
        self.scrolled_kontakty.set_size_request(100,100)
        self.scrolled_kontakty.set_max_content_width(50) 

        self.scrolled_kontakty.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        #Dodanie wiadmowsci
        self.scrolled_kontakty.add_with_viewport(self.grid_contact)

        self.kontakty.pack_start (self.scrolled_kontakty, True, True, 0)

        
     

        
        self.chat_window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.poziomo.pack_start(self.chat_window, True, True, 0)
        
   
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(600,300)
        self.scrolled_window.set_max_content_width(50) 
        self.scrolled_window.set_border_width(10) ##Odstęp po prawej

        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        #Dodanie wiadmowsci
        self.scrolled_window.add_with_viewport(self.add_messages())
        # add the scrolledwindow to the window
        #self.add(self.scrolled_window)   

        self.wysylanie = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        #self.add(vbox)

        #Okno do wpisywania tekstu
        self.entry_wysylanie = Gtk.Entry()
        self.entry_wysylanie.set_text("")
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        self.wysylanie.pack_start(self.entry_wysylanie, True, True, 0)

        #Przycisk do wysyłania tekstu
        self.send_button = Gtk.Button(label="Wyślij")
        self.send_button.connect("clicked", self.send_click)
        self.wysylanie.pack_start(self.send_button, True, True, 0)
        self.chat_window.pack_start(self.scrolled_window, True, True, 0)
        self.chat_window.pack_start(self.wysylanie, True, True, 0)

        self.profil = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
       
        self.send_button = Gtk.Button(label="Zmiana hasła")
        self.profil.pack_start(self.send_button, False, True, 0)
        self.send_button = Gtk.Button(label="Usuń konto")
        self.profil.pack_start(self.send_button, False, True, 0)
        

        self.poziomo.pack_start(self.profil, False, True, 0)
        
    def add_contact(self,nazwa):
       
        self.buttons.append(Gtk.Button(label=nazwa,xalign=0))

        self.grid_contact.add(self.buttons[-1])
        
    
    def add_message(self,wiad):
        
        if(wiad[1]==1):
            label = Gtk.Label(wiad[0])
            label.set_line_wrap(True)
            label.set_max_width_chars(5)
            label.set_alignment(0,0)
            
        else:
            label = Gtk.Label(wiad[0])
            label.set_line_wrap(True)
            label.set_max_width_chars(5)
            label.set_alignment(1,0)
        return label

    def add_messages(self):   
        self.lista_wiadomosci = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.lista_wiadomosci.set_homogeneous(False)

        messages = []
        for message in global_functions.income_messages_list:
            messages.append(message) 

        print(messages[-1])
        for message in messages:
            if(message[1]==1):
                label = Gtk.Label(message[0])
                label.set_line_wrap(True)
                label.set_max_width_chars(5)
                label.set_alignment(0,0)
                self.lista_wiadomosci.pack_start(label, True, False, 1)
            else:
                label = Gtk.Label(message[0])
                label.set_line_wrap(True)
                label.set_max_width_chars(5)
                label.set_alignment(1,0)
                self.lista_wiadomosci.pack_start(label, True, False, 1)
        
        
        return self.lista_wiadomosci


    def send_click(self, button):
        global income_messages_list
        wiadomosc = self.entry_wysylanie.get_text()
        print(wiadomosc)
        global_functions.income_messages_list.append([wiadomosc,2])
        self.lista_wiadomosci.pack_start(self.add_message([wiadomosc,2]), True, False, 1)
        self.entry_wysylanie.set_text("")
        self.entry_wysylanie.show_all()
        self.scrolled_window.show_all()

        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size()) #nie pokazuje ostatniej liniki 
        #samo get_upper lub get_page_size też działa (chyba)
        #-20 sprawia że nie pokazuje też przedostatniej ale +20 nic nie zmienia
        self.scrolled_window.show_all()

        
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
            grid.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
        
        return grid


