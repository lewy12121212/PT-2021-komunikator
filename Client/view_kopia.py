from typing import Tuple
import time
import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from client import Client
from response import Response
from request import Request
import sys
#import client

#Łukasz
from threading import Thread, Lock

c = Client()
resp = Response()
req = Request()
start_thread = 0

container = Gtk.Grid()

#Okno aplikacji
class App_view(Gtk.Window):

    

    def __init__(self):
       
        super(App_view, self).__init__(title="Komunikator")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)
        self.set_default_size(600, 250)

        self.add(container)
        container.show()

      
        #Okno logowania
        self.login_window = LoginWindow(self)
        container.add(self.login_window)
    
    def on_destroy(self, widget=None, *data):
        # return True --> no, don't close

        c.send("{'signal':'END','data':''}")
        
        
    def add_chat(self):
        #Okno czatu
        self.chat_window = FirstPage(self)
        container.add(self.chat_window)

    def add_register(self):
        #Okno czatu
        self.register_window = RegisterWindow(self)
        container.add(self.register_window)

     
        


class LoginWindow(Gtk.Grid):
    #Konstruktor - wywołuje okno logowania
    def __init__(self, parent_window):
        
        super().__init__()
        self.__parent_window = parent_window
        self.row_spacing = 10
        self.column_spacing = 10
        
        self.Login_window()
        
    #Pokazuje okno logowania
    def Show_login_window(self, *args):
        self.__parent_window.login_window.show_all()
        
    
    #Chowa okno logowania i pokazuje okno czatu
    def Show_chat_window(self, *args):
        self.__parent_window.chat_window.show_all()
        self.hide()

    #Chowa okno logowania i pokazuje okno rejestracji
    def Show_register_window(self, *args):
        self.__parent_window.register_window.show_all()
        self.hide()

 
    #Okno logowania
    def Login_window(self):

        #Pionowy box na elementy interfejsu
        vertical_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vertical_main_box)

        #Etykieta okna
        label_main_login = Gtk.Label("Logowanie")

        #Poziome okno do przechowyania elementów loginu
        horizontal_login_box = Gtk.Box(spacing=6)
        #Etykieta loginu
        label_login = Gtk.Label("Login: ")
        #Wpisywanie loginu
        self.entry_login = Gtk.Entry()
        self.entry_login.set_hexpand(False)
        self.entry_login.set_vexpand(False)
        self.entry_login.set_text("")  

        #Poziome okno do przechowyania elementów hasła
        horizontal_password_box = Gtk.Box(spacing=6)
        #Etykieta hasła
        label_haslo = Gtk.Label("Hasło: ")
        #Wpisywanie hasła
        self.entry_password = Gtk.Entry()
        self.entry_password.set_visibility(False)
        self.entry_password.set_hexpand(False)
        self.entry_password.set_vexpand(False)
        self.entry_password.set_text("")  
        
        #Dodawanie elementów loginu do boxa
        horizontal_login_box.set_halign(3)
        horizontal_login_box.pack_start(label_login, True, True, 0)
        horizontal_login_box.pack_start(self.entry_login, True, True, 0)
        
        #Dodawanie elementów hasła do boxa
        horizontal_password_box.set_halign(3)
        horizontal_password_box.pack_start(label_haslo, True, True, 0)
        horizontal_password_box.pack_start(self.entry_password, True, True, 0)

        label_main_login.set_hexpand(True)

        #Dodawanie elementów interfejsu
        vertical_main_box.pack_start(label_main_login, True, True, 0)
        vertical_main_box.pack_start(horizontal_login_box, True, True, 0)
        vertical_main_box.pack_start(horizontal_password_box, True, True, 0)

        #Poziomy box do przycisków
        horizontal_buttons_box = Gtk.Box(spacing=6)

        #Przycisk do logowania
        self.login_button = Gtk.Button(label="Zaloguj")
        self.login_button.connect("clicked", self.Click_login)
        self.login_button.set_halign(2)
        self.login_button.set_hexpand(True)
        horizontal_buttons_box.pack_start(self.login_button, True, True, 0)

        #Przycisk do rejestracji
        self.register_button = Gtk.Button(label="Zarejestruj się")
        self.register_button.connect("clicked", self.Click_register)
        self.register_button.set_halign(1)
        self.register_button.set_hexpand(True)
        horizontal_buttons_box.pack_start(self.register_button, False, True, 0)
        vertical_main_box.pack_start(horizontal_buttons_box, True, True, 0) 

    def Wrong_data(self):
        self.wrong_data_window = Gtk.Window()
        self.wrong_data_window.set_default_size(400, 100)

       
        label_wrong_data = Gtk.Label("Wpisano błędny login lub hasło")
        wrong_data_box = Gtk.VBox()
        wrong_data_box.pack_start(label_wrong_data,True,True, 1)
       
      
        self.wrong_data_window.add(wrong_data_box)
        self.wrong_data_window.show_all()   

        #W tym przypadku dopiero po 5 sek pojawia się tekst i w tym samym momecie zamyka okno
        #jak nie ma destroy to to widać 
        '''
        time.sleep(5)
        self.wrong_data_window.destroy() 
        '''

    #Kliknięcie przycisku do okna rejestracji
    def Click_register(self, button):
        self.__parent_window.add_register()
        #Zmiana okna na rejestrację
        self.Show_register_window()

    #Kliknięcie przycisku do zalogowania
    def Click_login(self, button):
        #Zrobić żeby było tylko jak są złe dane
        self.Wrong_data()
        #Zczytanie danych z wejścia
        login = self.entry_login.get_text()
        password = self.entry_password.get_text()

        #Przesłanie danych do logowania
        mess = req.logIn(login,password)
        c.send(str(mess))
        #Odebranie odpowiedzi serwera
        data = c.recv()
        print(data)

        if resp.Make_Response(data):
            #Poprawne zalogowanie
            print("ACK")
            c.login = login
            self.__parent_window.add_chat()
            #Przejście do okna czatu
            self.Show_chat_window()

        else:
            #Niepoprawne zalogowanie
            pass
           

class RegisterWindow(Gtk.Grid):
    #Konstruktor - wywołuje okno logowania
    def __init__(self, parent_window):
        
        super().__init__()
        self.__parent_window = parent_window
        self.row_spacing = 10
        self.column_spacing = 10
        
        self.Register_window()
        
    #Pokazanie okna logowania i schowanie okna rejestracji
    def Show_login_window(self, *args):
        self.__parent_window.login_window.show_all()
        self.hide()
        
 
    #Okno rejestracji
    def Register_window(self):

        vertical_interface_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vertical_interface_box)

        label_main = Gtk.Label("Rejestracja")

        vertical_labels_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_login = Gtk.Label("Login: ")
        label_login.set_halign(2)
        self.entry_login = Gtk.Entry()
        self.entry_login.set_hexpand(False)
        self.entry_login.set_vexpand(False)
        self.entry_login.set_text("")  

        vertical_entries_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_haslo = Gtk.Label("Hasło: ")
        label_haslo.set_halign(2)
        self.entry_password = Gtk.Entry()
        self.entry_password.set_visibility(False)
        self.entry_password.set_hexpand(False)
        self.entry_password.set_vexpand(False)
        self.entry_password.set_text("")  

        label_second_password = Gtk.Label("Powtórz hasło: ")
        label_second_password.set_halign(2)
        self.entry_second_password = Gtk.Entry()
        self.entry_second_password.set_visibility(False)
        self.entry_second_password.set_hexpand(False)
        self.entry_second_password.set_vexpand(False)
        self.entry_second_password.set_text("")  

        label_auth_key = Gtk.Label("Podaj ulubiony kolor: ")
        label_auth_key.set_halign(2)
        self.entry_auth_key = Gtk.Entry()
        self.entry_auth_key.set_hexpand(False)
        self.entry_auth_key.set_vexpand(False)
        self.entry_auth_key.set_text("")  
        
       
        vertical_labels_box.pack_start(label_login, True, True, 0)
        vertical_labels_box.pack_start(label_haslo, True, True, 0)
        vertical_labels_box.pack_start(label_second_password, True, True, 0)
        vertical_labels_box.pack_start(label_auth_key, True, True, 0)

        
        vertical_entries_box.pack_start(self.entry_login, True, True, 0)
        vertical_entries_box.pack_start(self.entry_password, True, True, 0)
        vertical_entries_box.pack_start(self.entry_second_password, True, True, 0)
        vertical_entries_box.pack_start(self.entry_auth_key, True, True, 0)

        
        horizontal_box = Gtk.Box(spacing=6)
        horizontal_box.set_halign(3)
        horizontal_box.pack_start(vertical_labels_box, True, True, 0)
        horizontal_box.pack_start(vertical_entries_box, True, True, 0)


        label_main.set_hexpand(True)
        vertical_interface_box.pack_start(label_main, True, True, 0)
        
        vertical_interface_box.pack_start(horizontal_box, True, True, 0)

        horizontal_button_box = Gtk.Box(spacing=6)
        horizontal_button_box.set_halign(3)

        self.register_button = Gtk.Button(label="Zarejestruj się")
        self.register_button.connect("clicked", self.Click_register)
        self.register_button.set_halign(3)
        self.register_button.set_hexpand(True)

        self.back_to_login_button = Gtk.Button(label="Powrót")
        self.back_to_login_button.connect("clicked", self.Click_back_to_login)
        self.back_to_login_button.set_halign(3)
        self.back_to_login_button.set_hexpand(True)

        horizontal_button_box.pack_start(self.register_button,False,True,0)
        horizontal_button_box.pack_start(self.back_to_login_button,False,True,0)
        vertical_interface_box.pack_start(horizontal_button_box, False, True, 0)

    def Click_back_to_login(self, button):  
        self.Show_login_window()  

    def Click_register(self, button):
        l = self.entry_login.get_text()
        h = self.entry_password.get_text()
        ph = self.entry_second_password.get_text()
        pyt = self.entry_auth_key.get_text()

        if(h!=ph):
            print("INNE HASLA")
        else:
           
            mess = req.register(l,h,pyt)
           

            c.send(str(mess))
        
            data = c.recv()
            print(data)
            if resp.Make_Response(data):
                print("ACK")


           
class FirstPage(Gtk.Grid):
    
    def __init__(self, parent_window):
       
        super().__init__()
        self.__parent_window = parent_window
        self.czat = global_functions.MsgList()
        self.uzytkownik = ""
        #Łukasz
        self.recv_thread = Thread(target=c.recv_thread, args=(self, ))
        print("ok")
        #self.recv_thread.start()
        #self.recv_thread.join()
        self.main_chat_window()
        print("okk")


    def Show_login_window(self, *args):
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
        
        print("okkk")
        self.recv_thread.start()
        self.poziomo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.add(self.poziomo)

        self.kontakty = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.poziomo.pack_start(self.kontakty, False, True, 0)
        self.label_kontakty = Gtk.Label("Lista kontaktów")
        self.label_kontakty.set_valign(1)
        self.kontakty.pack_start(self.label_kontakty, False, True, 0)

        self.guziki_kontakty = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.dodaj_kontakt = Gtk.Button(label="Dodaj kontakt")
        self.dodaj_kontakt.connect("clicked", self.click_add_contact)
        self.guziki_kontakty.pack_start(self.dodaj_kontakt, True, True, 0)
        self.usun_kontakt = Gtk.Button(label="Usuń kontakt")
        self.usun_kontakt.connect("clicked", self.click_delete_contact)
        self.guziki_kontakty.pack_start(self.usun_kontakt, True, True, 0)
        self.guziki_kontakty.set_valign(1)
        self.kontakty.pack_start(self.guziki_kontakty, False, True, 0)
        
        self.grid_contact = Gtk.Grid()
       
        self.buttons = [] 
        self.scrolled_kontakty = Gtk.ScrolledWindow()
        self.scrolled_kontakty.set_size_request(100,100)
        self.scrolled_kontakty.set_max_content_width(50) 

        self.scrolled_kontakty.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_kontakty.add_with_viewport(self.grid_contact)

        self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        
        #Dla każdego kontaktu z listy tworzy podpisany przycisk
        #Łukasz
        
        if global_functions.active_user_list:
            #Dla każdego kontaktu z listy tworzy podpisany przycisk
            for user in global_functions.active_user_list:
                self.buttons.append(Gtk.Button(label=user,xalign=0))
                self.buttons[-1].connect("clicked", self.click_contact)
                self.czat._append_user(user)

            self.grid_contact.add(self.buttons[0])
            for previous_button, button in zip(self.buttons,self.buttons[1:]):
                self.grid_contact.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
            
        self.kontakty.show_all()
         
                #Dodanie wiadmowsci
           

        
        #koniec if

        
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
        print("AAA")
        self.buttons.append(Gtk.Button(label=nazwa,xalign=0))
        self.buttons[-1].connect("clicked", self.click_contact)
        self.czat._append_user(nazwa)

        self.grid_contact.add(self.buttons[-1])
        self.scrolled_kontakty.add_with_viewport(self.grid_contact)

        self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        self.kontakty.show_all()
    
    def add_message(self,wiad):
        if(self.uzytkownik!=""):
            self.czat._append_msg(self.uzytkownik,wiad)
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
        return Gtk.Label("")

    def add_messages(self):   
        self.lista_wiadomosci = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.lista_wiadomosci.set_homogeneous(False)

        messages = []
        if(self.uzytkownik!=""):
            for message in self.czat._get_msg(self.uzytkownik):
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

    def click_delete_contact(self, button):
        self.window3 = Gtk.Window()
        self.window3.set_default_size(400, 170)

       
        label_delete = Gtk.Label("Podaj nazwę użytkownika:")
        self.entry_user = Gtk.Entry()
        self.entry_user.set_hexpand(False)
        self.entry_user.set_vexpand(False)
        self.entry_user.set_text("")  

        self.button_del = Gtk.Button("Usuń")

        pion = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL)
        vbox = Gtk.VBox()
        vbox.set_halign(3)
        vbox.pack_start(label_delete,True,False, 1)
        vbox.pack_start(self.entry_user,True, False, 1)
        self.button_del.connect("clicked", self.click_delete_user_name)
        #button_cancel = Gtk.Button("Cancel"
      
        hbox = Gtk.HBox()
        hbox.pack_start(self.button_del,True, False, 1)
        #hbox.pack_start(button_cancel,True, False, 1)
       
        pion.pack_start(vbox,True,False, 1)
        pion.pack_start(hbox,True,False, 1)
        self.window3.add(pion)
        self.window3.show_all()   

    def click_delete_user_name(self, button):
        print(self.entry_user.get_text())
        self.window3.destroy() 
        #Tu dodać nazwę użytkownika do znajomych     

    def click_add_contact(self, button):
        self.window2 = Gtk.Window()
        self.window2.set_default_size(400, 170)

       
        label_add = Gtk.Label("Podaj nazwę użytkownika:")
        self.entry_user = Gtk.Entry()
        self.entry_user.set_hexpand(False)
        self.entry_user.set_vexpand(False)
        self.entry_user.set_text("")  

        self.button_ok = Gtk.Button("Dodaj")

        pion = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL)
        vbox = Gtk.VBox()
        vbox.set_halign(3)
        vbox.pack_start(label_add,True,False, 1)
        vbox.pack_start(self.entry_user,True, False, 1)
        self.button_ok.connect("clicked", self.click_add_user_name)
        #button_cancel = Gtk.Button("Cancel"
      
        hbox = Gtk.HBox()
        hbox.pack_start(self.button_ok,True, False, 1)
        #hbox.pack_start(button_cancel,True, False, 1)
       
        pion.pack_start(vbox,True,False, 1)
        pion.pack_start(hbox,True,False, 1)
        self.window2.add(pion)
        self.window2.show_all()   

    def click_add_user_name(self, button):
        print(self.entry_user.get_text())
        self.window2.destroy() 
        #Tu dodać nazwę użytkownika do znajomych 
          

    def click_contact(self,button):
        self.uzytkownik = button.get_label()
        print(button.get_label())

    def send_click(self, button):
        global income_messages_list
        wiadomosc = self.entry_wysylanie.get_text()
        print(wiadomosc)
        t = time.localtime()
        global_functions.income_messages_list.append([str(time.strftime("%H:%M:%S", t) + "\nTy:\n" + wiadomosc),2])
        self.lista_wiadomosci.pack_start(self.add_message([str(time.strftime("%H:%M:%S", t) + "\nTy:\n" + wiadomosc),2]), True, False, 1)
        self.entry_wysylanie.set_text("")
        self.entry_wysylanie.show_all()
        #self.scrolled_window.show_all()


        #ŁUKASZ
        #wysyłanie wiadomości
        c.send(req.message(self.uzytkownik,c.login,wiadomosc))

        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size()) #nie pokazuje ostatniej liniki 
        #samo get_upper lub get_page_size też działa (chyba)
        #-20 sprawia że nie pokazuje też przedostatniej ale +20 nic nie zmienia
        self.scrolled_window.show_all()

    #Łukasz
    def refresh_chat(self, mess):
        print("LLLLLLL: ",mess)
        self.lista_wiadomosci.pack_start(self.add_message(mess), True, False, 1)
        self.scrolled_window.show_all()


    def active_users(self):
       
        for user in global_functions.active_user_list:
            self.buttons.append(Gtk.Button(label=user,xalign=0))
            self.buttons[-1].connect("clicked", self.click_contact)
            self.czat._append_user(user)

        self.grid_contact.add(self.buttons[0])
        for previous_button, button in zip(self.buttons,self.buttons[1:]):
            self.grid_contact.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
        
        #Dodanie wiadmowsci
        self.scrolled_kontakty.add_with_viewport(self.grid_contact)

        self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        
        self.kontakty.show_all()



    def refresh_contact_list(self,nazwa):
        #self.grid_contact = Gtk.Grid()
        #self.buttons = [] 
            
        self.buttons.append(Gtk.Button(label=nazwa,xalign=0))
        self.buttons[-1].connect("clicked", self.click_contact)
        self.czat._append_user(nazwa)
        if(len(self.buttons)==1):
            self.grid_contact.add(self.buttons[0])
        else:
            self.grid_contact.attach_next_to(self.buttons[-1], self.buttons[-2], Gtk.PositionType.BOTTOM, 1, 1)
        #self.grid_contact.show_all()
        '''    
        self.scrolled_kontakty = Gtk.ScrolledWindow()
        self.scrolled_kontakty.set_size_request(100,100)
        self.scrolled_kontakty.set_max_content_width(50) 

        self.scrolled_kontakty.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        '''
        #Dodanie wiadmowsci
        self.scrolled_kontakty.add_with_viewport(self.grid_contact)
        #self.scrolled_kontakty.show_all()
        self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        self.kontakty.show_all()


    #Lista kontaktów
    def contact_list(self):
        grid = Gtk.Grid()
        self.add(grid)
        
        buttons = [] 
        
        #Dla każdego kontaktu z listy tworzy podpisany przycisk
        for user in global_functions.active_user_list:
            buttons.append(Gtk.Button(label=user))
            self.buttons[-1].connect("clicked", self.click_contact)
            self.czat._append_user(user)

        grid.add(buttons[0])
        for previous_button, button in zip(buttons,buttons[1:]):
            grid.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
        
        return grid

   
			


