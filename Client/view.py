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

class app_viev(Gtk.Window):
    def __init__(self):
        super(app_viev, self).__init__(title="Komunikator")
        self.connect("destroy", Gtk.main_quit)#
        self.set_border_width(20)
        self.set_default_size(800, 400)

        container = Gtk.Box()
        self.add(container)
        container.show()

        self.main = Main(self)
        container.add(self.main)

        self.first_page = FirstPage(self)
        container.add(self.first_page)
        


class Main(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(spacing=10)
        self.__parent_window = parent_window
        self.login()


    def start_new_game(self, *args):
        self.__parent_window.first_page.show_all()
        self.hide()

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
        vbox.pack_start(self.send_button, True, True, 0)
        return vbox

    def on_login_click(self, button):
        
        e = self.entry.get_text()
        o = self.entry2.get_text()

        #Tu coś w stylu 
        #czy_poprawne_logowanie()
        # jeśli tak to 

        
        mess = {"signal":"LOG", "data":{"login":e,"password":o}}
        
        c.send(str(mess))
        data = c.recv()
        print(data)
        if resp.Make_Response(data):
            c.login = e
            self.start_new_game()
        else:
            print(mess["data"])

        #print(resp)
        #print("Login: ", e)
        #print("Haslo: ", o)
        #print("Zalogowano")
        

    '''def registration(self):
        login = Gtk.Grid(row_spacing = 10,column_spacing = 10)
        self.add(login)
        
        login.add(self.login_label())
        login.attach(self.login_entry(), 0, 1, 1, 1)
        login.attach(self.password_entry(), 0, Gtk.PositionType.BOTTOM, 1, 2)   
        login.attach(self.login_button("Zarejestruj"), 1, 1, 1, 1) 
    '''

    def password_entry(self):
        vboxa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.add(vboxa)
        vboxa.set_hexpand(False)
        label = Gtk.Label("Hasło: ")
        #label.set_alignment(0.5,0)
        vboxa.pack_start(label, False, False, 20)

        #Okno do wpisywania tekstu
        self.entry2 = Gtk.Entry()
        self.entry2.set_text("")
        #self.entry.set_alignment(0)
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        vboxa.pack_start(self.entry2, False, False, 1) 
        return vboxa   

    def login_entry(self):
        vboxa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.add(vboxa)
        vboxa.set_hexpand(False)
        label = Gtk.Label("Login: ")
        #label.set_alignment(0.5,0)
        vboxa.pack_start(label, False, False, 20)

        #Okno do wpisywania tekstu
        #self.le()
        #self.entry.set_alignment(0)
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        vboxa.pack_start(self.le(), False, False, 1) 

        return vboxa

    def le(self): 
        self.entry = Gtk.Entry()
        self.entry.set_text("")  
        return self.entry

    def login_label(self): 
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
    
        label = Gtk.Label("Logowanie")
        label.set_hexpand(True)
        #label.set_alignment(1,0)
        vbox.pack_start(label, True, True, 0)
        self.add(vbox)
        return vbox  


class FirstPage(Gtk.Box):
    
    def __init__(self, parent_window):
       
        super().__init__(spacing=10)
        self.__parent_window = parent_window
        aaa = self.main_chat_window()
    

    def return_start_page(self, *args):
        self.__parent_window.main.show_all()
        self.hide()

    def refresh_chat(self, *args):
        #self.main_chat_window().remove_all()
        '''
        app_viev.container.remove(app_viev.container.first_page)
        first_page = FirstPage(self)
        app_viev.container.add(first_page)
        
        '''
        
        self.aaa = self.main_chat_window()
        self.__parent_window.first_page.show_all()
    
    

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


    def main_chat_window(self):
        
        print("OKNO")
        #self.remove(pom)
        self.pom = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=6)
        #pom = Gtk.Grid(row_spacing = 5,column_spacing = 10)
        
        #pom to okno główne
        #contacts zawiera rzeczy związane z listą kontaktów
        self.contacts = Gtk.Grid(row_spacing = 5)
        self.pom.add(self.contacts)
        self.contacts.add(self.contact_tabel())
        '''
        contacts.attach(self.contact_buttons(), 0, 1, 1, 1)
        contacts.attach(self.contact_list(), 0, 2, 1, 2)
        '''
        self.contacts.add(self.contact_buttons())
        self.contacts.add(self.contact_list())

        #Okno czatu 
        self.chat_window = Gtk.Grid(row_spacing = 5)
        self.pom.add(self.chat_window)
        '''
        chat_window.attach(self.entry_to_send(), 1, 2, 1, 1)
        chat_window.attach(self.messages_print(), 1,0, 1, 1)
        '''
        self.chat_window.add(self.entry_to_send())
        self.chat_window.add(self.messages_print())


        self.profile = Gtk.Grid(row_spacing = 5)
        self.pom.add(self.profile)
        self.profile.add(self.profile_buttons())

        self.pom.add(self.contacts)
        '''
        pom.attach(chat_window, 1, 0, 1, 1)
        pom.attach(profile, 1, 1, 1, 1)
        '''
        self.pom.add(self.chat_window)
        self.pom.add(self.profile)
        self.add(self.pom)
        return self.pom

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

    def messages_print(self):
    
        #hbox = Gtk.Box(spacing = 10)
        #hbox.set_homogeneous(False)
       
       # hbox.pack_start(vbox_left, True, True, 0)
       
    
        #Okno do scrolowania
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(600,200)
        self.scrolled_window.set_max_content_width(50) 
        self.scrolled_window.set_border_width(10) ##Odstęp po prawej

        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

      
        #Dodanie wiadmowsci
        self.scrolled_window.add_with_viewport(self.add_messages())
        
        # add the scrolledwindow to the window
        self.add(self.scrolled_window)   

        #self.add(hbox)
        return self.scrolled_window  


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
        self.send_button.connect("clicked", self.send_click)
        vbox.pack_start(self.send_button, True, True, 0)

        return vbox

    def send_click(self, button):
        global income_messages_list
        wiadomosc = self.entry.get_text()
        print(wiadomosc)
        global_functions.income_messages_list.append([wiadomosc,2])
        #print(self.main_chat_window().get_childern())
        #self.callback_remove()
        self.lista_wiadomosci.pack_start(self.add_message([wiadomosc,2]), True, False, 1)
        self.scrolled_window.show_all()
   
        
       

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


