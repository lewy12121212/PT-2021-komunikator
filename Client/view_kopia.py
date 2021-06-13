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
from split_msg import main_split
import sys
#import client

#Łukasz
from threading import Thread, Lock

c = Client()
resp = Response()
req = Request()
start_thread = 0
login = ''
inne = False
container = Gtk.Grid()
th = []
new_mess_info = False

#Okno aplikacji
class App_view(Gtk.Window):

    

    def __init__(self):
       
        super(App_view, self).__init__(title="Komunikator")
        self.connect("delete-event", self.on_destroy)
        self.set_border_width(20)
        self.set_default_size(600, 250)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.recv_thread = Thread(target=c.recv_thread, args=(self, resp))
        self.recv_thread.start()
        #self.alert = Alert_Window(self)
        self.add(container)
        container.show()
        self.alert_text = ''
      
        #Okno logowania
        self.login_window = LoginWindow(self)
        container.add(self.login_window) 

        #c.recv_thread(self, resp)
        
    def add_chat(self):
        #Okno czatu
        self.chat_window = FirstPage(self)
        container.add(self.chat_window)

    def add_register(self):
        #Okno rejestracji
        self.register_window = RegisterWindow(self)
        container.add(self.register_window)

    def add_change(self):
        self.change_window = ChangePasswordWindow(self)
        container.add(self.change_window)

    def show_alert(alert_text):
        print("było tu")
        alert = Alert_Window.Show_alert_window(alert_text)
        print("było tu")

    def on_destroy(self, widget=None, *data):
        # return True --> no, don't close
        
        c.send("{'signal':'END','data':''}")
        self.connect("destroy", Gtk.main_quit)
        c.close()
        #Gtk.main_quit
        return False 


     
        


class LoginWindow(Gtk.Grid):
    #Konstruktor - wywołuje okno logowania
    def __init__(self, parent_window):
        
        super().__init__()
        self.__parent_window = parent_window
        self.row_spacing = 10
        self.column_spacing = 10
        #self.recv_thread = Thread(target=c.recv_thread, args=(self, ))
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
        priority = Gtk.STYLE_PROVIDER_PRIORITY_USER
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, priority)
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

    #Chowa okno logowania i pokazuje okno zmiany hasła
    def Show_change_window(self, *args):
        self.__parent_window.change_window.show_all()
        self.hide()

 
    #Okno logowania
    def Login_window(self):

        #Pionowy box na elementy interfejsu
        vertical_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vertical_main_box)

        #Etykieta okna
        label_main_login = Gtk.Label("Logowanie",name="white_label")

        #Poziome okno do przechowyania elementów loginu
        horizontal_login_box = Gtk.Box(spacing=6)
        #Etykieta loginu
        label_login = Gtk.Label("Login: ",name="white_label")
        #Wpisywanie loginu
        self.entry_login = Gtk.Entry()
        self.entry_login.set_max_length(32)
        self.entry_login.set_hexpand(False)
        self.entry_login.set_vexpand(False)
        self.entry_login.set_text("")  

        #Poziome okno do przechowyania elementów hasła
        horizontal_password_box = Gtk.Box(spacing=6)
        #Etykieta hasła
        label_haslo = Gtk.Label("Hasło: ",name="white_label")
        #Wpisywanie hasła
        self.entry_password = Gtk.Entry()
        self.entry_password.set_max_length(32)
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
        self.login_button = Gtk.Button(label = "Zaloguj",name="button_one")
        #self.login_button.get_style_context().add_class("suggested-action")
        self.login_button.connect("clicked", self.Click_login)
        self.login_button.set_halign(2)
        self.login_button.set_hexpand(True)
        horizontal_buttons_box.pack_start(self.login_button, True, True, 0)

        #Przycisk do rejestracji
        self.register_button = Gtk.Button(label="Zarejestruj się",name="button_one")
        self.register_button.connect("clicked", self.Click_register)
        self.register_button.set_halign(1)
        self.register_button.set_hexpand(True)
        horizontal_buttons_box.pack_start(self.register_button, False, True, 0)
        vertical_main_box.pack_start(horizontal_buttons_box, True, True, 0) 

        #Przycisk do pytania kontrolnego
        self.reset_button = Gtk.Button(label="Zresetuj hasło",name="button_one")
        self.reset_button.connect("clicked", self.Click_reset)
        self.reset_button.set_halign(3)
        self.reset_button.set_hexpand(True)
        vertical_main_box.pack_start(self.reset_button, True, True, 0) 


    def Click_reset(self,button):
        self.__parent_window.add_change()
        #Zmiana okna na rejestrację
        self.Show_change_window()

    #Kliknięcie przycisku do okna rejestracji
    def Click_register(self, button):
        self.__parent_window.add_register()
        #Zmiana okna na rejestrację
        self.Show_register_window()

    #Kliknięcie przycisku do zalogowania
    def Click_login(self, button):
        #Zrobić żeby było tylko jak są złe dane
        #self.Wrong_data(tekst)
        global login
        #button.get_style_context().remove_class("suggested-action")
        #Zczytanie danych z wejścia
        login = self.entry_login.get_text()
        password = self.entry_password.get_text()
        if login == '':
            Alert_Window.Show_alert_window("Nie podano loginu.")
        elif password == '':
            Alert_Window.Show_alert_window("Nie podano hasła.")
        else:
    
            mess = req.logIn(login,password)
            c.send(str(mess))
            time.sleep(0.4)

            if not resp.accept:
                if resp.exists:
                    Alert_Window.Show_alert_window("Użytkownik jest już zalogowany.")
                else:
                    Alert_Window.Show_alert_window("Błędny login lub hasło.")

    
    def After_Login(self):
   
        print("ACK")
        global login
        c.login = login
        self.__parent_window.add_chat()
        #Przejście do okna czatu
        #self.recv_thread.start()
        self.Show_chat_window()
        
    

class ChangePasswordWindow(Gtk.Grid):
    #Konstruktor - wywołuje okno zmiany hasła
    def __init__(self, parent_window):
        
        super().__init__()
        self.__parent_window = parent_window
        self.row_spacing = 10
        self.column_spacing = 10
        
        self.Change_password()
    
    #Pokazanie okna logowania i schowanie okna rejestracji
    def Show_login_window(self, *args):
        self.__parent_window.login_window.show_all()
        self.hide()

    def Change_password(self):
        vertical_interface_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vertical_interface_box)

        label_main = Gtk.Label("Zresetuj hasło",name="white_label")

        vertical_labels_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_login = Gtk.Label("Login: ",name="white_label")
        label_login.set_halign(2)
        self.entry_login = Gtk.Entry()
        self.entry_login.set_max_length(32)
        self.entry_login.set_hexpand(False)
        self.entry_login.set_vexpand(False)
        self.entry_login.set_text("")  

        vertical_entries_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_haslo = Gtk.Label("Nowe hasło: ",name="white_label")
        label_haslo.set_halign(2)
        self.entry_password = Gtk.Entry()
        self.entry_password.set_max_length(32)
        self.entry_password.set_visibility(False)
        self.entry_password.set_hexpand(False)
        self.entry_password.set_vexpand(False)
        self.entry_password.set_text("")  

        label_second_password = Gtk.Label("Powtórz nowe hasło: ",name="white_label")
        label_second_password.set_halign(2)
        self.entry_second_password = Gtk.Entry()
        self.entry_second_password.set_max_length(32)
        self.entry_second_password.set_visibility(False)
        self.entry_second_password.set_hexpand(False)
        self.entry_second_password.set_vexpand(False)
        self.entry_second_password.set_text("")  

        label_auth_key = Gtk.Label("Podaj nazwisko panieńskie matki: ",name="white_label")
        label_auth_key.set_halign(2)
        self.entry_auth_key = Gtk.Entry()
        self.entry_auth_key.set_max_length(32)
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

        self.register_button = Gtk.Button(label="Zmień hasło",name="button_one")
        self.register_button.connect("clicked", self.Click_reset_password)
        self.register_button.set_halign(3)
        self.register_button.set_hexpand(True)

        self.back_to_login_button = Gtk.Button(label="Powrót",name="button_one")
        self.back_to_login_button.connect("clicked", self.Click_back_to_login)
        self.back_to_login_button.set_halign(3)
        self.back_to_login_button.set_hexpand(True)

        horizontal_button_box.pack_start(self.register_button,False,True,0)
        horizontal_button_box.pack_start(self.back_to_login_button,False,True,0)
        vertical_interface_box.pack_start(horizontal_button_box, False, True, 0)

    def Click_reset_password(self, button): 
        ####
        data = req.reset_password(self.entry_login.get_text(),self.entry_password.get_text(), self.entry_auth_key.get_text())
        if(self.entry_password.get_text() != self.entry_second_password.get_text()):
            alert = Alert_Window.Show_alert_window("Błędnie powtórzono hasło.")
        elif(len(self.entry_password.get_text())<8):
            alert = Alert_Window.Show_alert_window("Podane hasło jest zbyt krótkie.")
        else:
            c.send(data)
            time.sleep(0.4)
            #print("kacper")
            if resp.accept:
                #print("kacper")
                Alert_Window.Show_alert_window("Pomyślnie zresetowano hasło.")
            else:
                if resp.exists:
                    Alert_Window.Show_alert_window("Użytkownik nie istnieje.")
                    resp.exists = False   
                    #print("kacper")
                else:
                    Alert_Window.Show_alert_window("Błędna odpowiedź na pytanie autoryzacyjne.")



    def Click_back_to_login(self, button):      
         self.Show_login_window()  

    def Click_ok(self, button):
        self.wrong_data_window.destroy()
   
           

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

        label_main = Gtk.Label("Rejestracja",name="white_label")

        vertical_labels_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_login = Gtk.Label("Login: ",name="white_label")
        label_login.set_halign(2)
        self.entry_login = Gtk.Entry()
        self.entry_login.set_max_length(32)
        self.entry_login.set_hexpand(False)
        self.entry_login.set_vexpand(False)
        self.entry_login.set_text("")  

        vertical_entries_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_haslo = Gtk.Label("Hasło: ",name="white_label")
        label_haslo.set_halign(2)
        self.entry_password = Gtk.Entry()
        self.entry_password.set_visibility(False)
        self.entry_password.set_max_length(32)
        self.entry_password.set_hexpand(False)
        self.entry_password.set_vexpand(False)
        self.entry_password.set_text("")  

        label_second_password = Gtk.Label("Powtórz hasło: ",name="white_label")
        label_second_password.set_halign(2)
        self.entry_second_password = Gtk.Entry()
        self.entry_second_password.set_max_length(32)
        self.entry_second_password.set_visibility(False)
        self.entry_second_password.set_hexpand(False)
        self.entry_second_password.set_vexpand(False)
        self.entry_second_password.set_text("")  

        label_auth_key = Gtk.Label("Podaj nazwisko panieńskie matki: ",name="white_label")
        label_auth_key.set_halign(2)
        self.entry_auth_key = Gtk.Entry()
        self.entry_auth_key.set_max_length(32)
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

        self.register_button = Gtk.Button(label="Zarejestruj się",name="button_one")
        self.register_button.connect("clicked", self.Click_register)
        self.register_button.set_halign(3)
        self.register_button.set_hexpand(True)

        self.back_to_login_button = Gtk.Button(label="Powrót",name="button_one")
        self.back_to_login_button.connect("clicked", self.Click_back_to_login)
        self.back_to_login_button.set_halign(3)
        self.back_to_login_button.set_hexpand(True)

        horizontal_button_box.pack_start(self.register_button,False,True,0)
        horizontal_button_box.pack_start(self.back_to_login_button,False,True,0)
        vertical_interface_box.pack_start(horizontal_button_box, False, True, 0)

    def Click_back_to_login(self, button):  
        self.Show_login_window()  

    def Click_register(self, button):
        ###
        #self.Show_alert_window(tekst)
        l = self.entry_login.get_text()
        h = self.entry_password.get_text()
        ph = self.entry_second_password.get_text()
        pyt = self.entry_auth_key.get_text()

        if(h!=ph):
            print("INNE HASLA")
            alert = Alert_Window.Show_alert_window("Błędnie powtórzono hasło")
        elif len(h)<8:
            alert = Alert_Window.Show_alert_window("Podane hasło jest zbyt krótkie.")
            #self.Show_alert_window("Podane hasło jest zbyt krótkie.")
        elif len(l)>32:
            alert = Alert_Window.Show_alert_window("Twój login jest zbyt długi.")

            #self.Show_alert_window("Twój login jest zbyt długi.")
        else:
           
            mess = req.register(l,h,pyt)
           

            c.send(str(mess))
            time.sleep(0.4)
            if resp.accept:
                Alert_Window.Show_alert_window("Poprawnie dodano konto.")
            else:
                Alert_Window.Show_alert_window("Konto już istnieje.")


           
class FirstPage(Gtk.Grid):
    
    def __init__(self, parent_window):
       
        super().__init__()
        self.__parent_window = parent_window
        self.czat = global_functions.MsgList()
        self.uzytkownik = ""
        

        self.main_chat_window()

    def Show_login_window(self, *args):
        self.__parent_window.login_window.show_all()
        self.hide()

    def contact_change(self):
        vboxa = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.add(vboxa)
        vboxa.set_hexpand(True)
        label = Gtk.Label("Podaj nazwę użytkownika: ",name="white_label")
        vboxa.pack_start(label, True, True, 0)

       
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        #Maksymalna dlugość wiadomości
        #self.entry.set_max_length (512)
        vboxa.pack_start(self.entry, True, True, 0)
         


    def main_chat_window(self):
        
       
        #self.recv_thread.start()
        self.poziomo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.add(self.poziomo)

        self.kontakty = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.poziomo.pack_start(self.kontakty, False, True, 0)
        self.label_kontakty = Gtk.Label("Lista aktywnych kontaktów",name="white_label")
        self.label_kontakty.set_valign(1)
        self.kontakty.pack_start(self.label_kontakty, False, True, 0)

        self.grid_contact = Gtk.Grid(name='contact_grid')
       
        self.buttons = [] 
        self.scrolled_kontakty = Gtk.ScrolledWindow()
        self.scrolled_kontakty.set_size_request(100,100)
        self.scrolled_kontakty.set_max_content_width(50) 

        self.scrolled_kontakty.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_kontakty.add(self.grid_contact)

        self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)

        self.guziki_kontakty = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.dodaj_kontakt = Gtk.Button(label="Dodaj kontakt",name="button_one")
        self.dodaj_kontakt.connect("clicked", self.click_add_contact)
        self.guziki_kontakty.pack_start(self.dodaj_kontakt, True, True, 0)
        self.usun_kontakt = Gtk.Button(label="Usuń kontakt",name="button_one")
        self.usun_kontakt.connect("clicked", self.click_delete_contact)
        self.guziki_kontakty.pack_start(self.usun_kontakt, True, True, 0)
        self.guziki_kontakty.set_valign(1)
        
        self.guziki_kontakty_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.wyswietl_wszystkie = Gtk.Button(label="Wyświetl wszystkie kontakty",name="button_one")
        self.wyswietl_wszystkie.connect("clicked", self.click_show_all_contacts)
        self.guziki_kontakty_2.pack_start(self.wyswietl_wszystkie, True, True, 0)
        self.guziki_kontakty_2.set_valign(1)
        self.kontakty.pack_start(self.guziki_kontakty, False, True, 0)
        self.kontakty.pack_start(self.guziki_kontakty_2, False, True, 0)
        

        
        
        
        if global_functions.active_user_list:
            #Dla każdego kontaktu z listy tworzy podpisany przycisk
            for user in global_functions.active_user_list:
                self.buttons.append(Gtk.Button(label=user,xalign=1, valign = 1, halign = 1,name="button_contact"))
                self.buttons[-1].connect("clicked", self.click_contact)
                self.czat._append_user(user)

            self.grid_contact.add(self.buttons[0])
            for previous_button, button in zip(self.buttons,self.buttons[1:]):
                self.grid_contact.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
            
        self.kontakty.show_all()
         

        
        self.chat_window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.poziomo.pack_start(self.chat_window, False, False, 0)
        self.chat_name = Gtk.Label(name="white_label")
        self.chat_name.set_text("")
   
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(600,300)
        self.scrolled_window.set_vexpand(False)
        self.scrolled_window.set_max_content_width(10) 
        #self.scrolled_window.vexpand(False)
       
        self.scrolled_window.set_border_width(10) ##Odstęp po prawej
        #self.scrolled_window.set_vexpand(False)
        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        #Dodanie wiadmowsci
        self.scrolled_window.add(self.add_messages())
      

        self.wysylanie = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
       
        #Okno do wpisywania tekstu
        self.entry_wysylanie = Gtk.Entry()
        self.entry_wysylanie.set_text("")
        #Maksymalna dlugość wiadomości
        self.entry_wysylanie.set_max_length(350)
        self.wysylanie.pack_start(self.entry_wysylanie, True, True, 0)

        #Przycisk do wysyłania tekstu
        self.send_button = Gtk.Button(label="Wyślij",name="button_one")
        self.send_button.connect("clicked", self.send_click)
        self.wysylanie.pack_start(self.send_button, True, True, 0)

        self.chat_window.pack_start(self.chat_name,True,True,0)
        self.chat_window.pack_start(self.scrolled_window, False, False, 0)
        self.chat_window.pack_start(self.wysylanie, True, True, 0)

        self.profil = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
       
        self.change_button = Gtk.Button(label="Zmiana hasła",name="button_one")
        self.profil.pack_start(self.change_button, False, True, 0)
        self.change_button.connect("clicked", self.change_click)

        self.delete_acc_button = Gtk.Button(label="Usuń konto",name="button_one")
        self.profil.pack_start(self.delete_acc_button, False, True, 0)
        self.delete_acc_button.connect("clicked", self.delete_acc_click)
        
        self.log_out_button = Gtk.Button(label="Wyloguj",name="button_one")
        self.profil.pack_start(self.log_out_button, False, True, 0)
        self.log_out_button.connect("clicked", self.log_out_click)

        self.poziomo.pack_start(self.profil, False, True, 0)

    def click_show_all_contacts(self,button):
        self.window6 = Gtk.Window()
        self.window6.set_default_size(400, 300)
        self.window6.set_position(Gtk.WindowPosition.CENTER)
        vertical_interface_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
       

        label_main = Gtk.Label("Kontakty",name="white_label_title")
   
       
        label_main.set_hexpand(True)
        vertical_interface_box.pack_start(label_main, True, True, 0)
        if global_functions.contact_user_list:
            
            for user in global_functions.contact_user_list:
                print(user)
                lab = Gtk.Label(user,name="white_label_contact")
                vertical_interface_box.pack_start(lab, True, True, 0)
    

        vertical_interface_box.set_valign(1)
        self.window6.add(vertical_interface_box)
        
       
       
        self.window6.show_all()


    def log_out_click(self, button):
        print("wyloguj")
        #dodać wylogowywanie\
        '''self.scrolled_kontakty.remove(self.scrolled_kontakty.get_child())
        self.grid_contact = Gtk.Grid()
        self.scrolled_kontakty.add(self.grid_contact)
        '''
        #self.buttons.clear()
        for usr in self.buttons:
            pom = usr.get_label()
            global_functions.active_user_list.remove(pom)            
            self.refresh_contact_list_out(pom)
        
        global_functions.contact_user_list.clear()
        
        
        global login
        c.send(req.logOut(c.login))
        c.login = ''
        login = ""
        
        self.__parent_window.login_window.entry_login.set_text("")
        self.__parent_window.login_window.entry_password.set_text("") 
        self.Show_login_window()     

    def delete_acc_click(self, button):
        self.window5 = Gtk.Window()
        self.window5.set_default_size(400, 270)
        self.window5.set_position(Gtk.WindowPosition.CENTER)
        vertical_interface_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
       

        label_main = Gtk.Label("Usuń konto",name="white_label")

        vertical_labels_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
       

        vertical_entries_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_old_haslo = Gtk.Label("Podaj hasło: ",name="white_label")
        label_old_haslo.set_halign(2)
        self.old_entry_password = Gtk.Entry()
        self.old_entry_password.set_max_length(32)
        self.old_entry_password.set_visibility(False)
        self.old_entry_password.set_hexpand(False)
        self.old_entry_password.set_vexpand(False)
        self.old_entry_password.set_text("")  

        label_haslo = Gtk.Label("Powtórz hasło: ",name="white_label")
        label_haslo.set_halign(2)
        self.entry_password = Gtk.Entry()
        self.entry_password.set_max_length(32)
        self.entry_password.set_visibility(False)
        self.entry_password.set_hexpand(False)
        self.entry_password.set_vexpand(False)
        self.entry_password.set_text("")  


        label_auth_key = Gtk.Label("Podaj nazwisko panieńskie matki: ",name="white_label")
        label_auth_key.set_halign(2)
        self.entry_auth_key = Gtk.Entry()
        self.entry_auth_key.set_max_length(32)
        self.entry_auth_key.set_hexpand(False)
        self.entry_auth_key.set_vexpand(False)
        self.entry_auth_key.set_text("")  
            
        
        vertical_labels_box.pack_start(label_old_haslo, True, True, 0)
        vertical_labels_box.pack_start(label_haslo, True, True, 0)
        vertical_labels_box.pack_start(label_auth_key, True, True, 0)
        #vertical_labels_box.set_valign(3)
            
        vertical_entries_box.pack_start(self.old_entry_password, True, True, 0)
        vertical_entries_box.pack_start(self.entry_password, True, True, 0)
        vertical_entries_box.pack_start(self.entry_auth_key, True, True, 0)
        #vertical_entries_box.set_valign(3)
            
        horizontal_box = Gtk.Box(spacing=6)
        horizontal_box.set_halign(3)
        horizontal_box.pack_start(vertical_labels_box, True, True, 0)
        horizontal_box.pack_start(vertical_entries_box, True, True, 0)


        label_main.set_hexpand(True)
        vertical_interface_box.pack_start(label_main, True, True, 0)
            
        vertical_interface_box.pack_start(horizontal_box, True, True, 0)
        vertical_interface_box.set_valign(3)
        horizontal_button_box = Gtk.Box(spacing=6)
        horizontal_button_box.set_halign(3)

        self.register_button = Gtk.Button(label="Usuń konto",name="button_one")
        self.register_button.connect("clicked", self.Click_delete_account_ok)
        self.register_button.set_halign(3)
        self.register_button.set_hexpand(True)

        self.back_to_login_button = Gtk.Button(label="Powrót",name="button_one")
        self.back_to_login_button.connect("clicked", self.Close_delete_acc)
        self.back_to_login_button.set_halign(3)
        self.back_to_login_button.set_hexpand(True)

        horizontal_button_box.pack_start(self.register_button,False,True,0)
        horizontal_button_box.pack_start(self.back_to_login_button,False,True,0)
        vertical_interface_box.pack_start(horizontal_button_box, False, True, 0)
        self.window5.add(vertical_interface_box)
        self.window5.show_all()

    def Click_delete_account_ok(self, button): 
        #jeśli jakiś błąd
        #self.Show_alert_window(tekst_bledu)


        #dodać wylogowanie użytwkownika
        global login
        data = req.delete_account(login,self.entry_password.get_text(), self.entry_auth_key.get_text())
        c.send(data)
        

        time.sleep(0.4)
        if resp.accept:
            Alert_Window.Show_alert_window("Twoje konto zostało usunięte.")
            self.window5.destroy()  
            self.__parent_window.login_window.entry_login.set_text("")
            self.__parent_window.login_window.entry_password.set_text("") 
            self.Show_login_window()
        else:
            Alert_Window.Show_alert_window("Bledna odpowiedz autoryzacyjna lub obecne haslo.")

    def Close_delete_acc(self,button):
       
        self.window5.destroy()    

    def change_click(self, button):
        self.window4 = Gtk.Window()
        self.window4.set_default_size(400, 270)
        self.window4.set_position(Gtk.WindowPosition.CENTER)
        vertical_interface_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        #self.add(vertical_interface_box)

        label_main = Gtk.Label("Zmień hasło",name="white_label")

        vertical_labels_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
       

        vertical_entries_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label_old_haslo = Gtk.Label("Aktualne hasło: ",name="white_label")
        label_old_haslo.set_halign(2)
        self.old_entry_password = Gtk.Entry()
        self.old_entry_password.set_max_length(32)
        self.old_entry_password.set_visibility(False)
        self.old_entry_password.set_hexpand(False)
        self.old_entry_password.set_vexpand(False)
        self.old_entry_password.set_text("")  

        label_haslo = Gtk.Label("Nowe hasło: ",name="white_label")
        label_haslo.set_halign(2)
        self.entry_password = Gtk.Entry()
        self.entry_password.set_max_length(32)
        self.entry_password.set_visibility(False)
        self.entry_password.set_hexpand(False)
        self.entry_password.set_vexpand(False)
        self.entry_password.set_text("")  

        label_second_password = Gtk.Label("Powtórz nowe hasło: ",name="white_label")
        label_second_password.set_halign(2)
        self.entry_second_password = Gtk.Entry()
        self.entry_second_password.set_max_length(32)
        self.entry_second_password.set_visibility(False)
        self.entry_second_password.set_hexpand(False)
        self.entry_second_password.set_vexpand(False)
        self.entry_second_password.set_text("")  

        label_auth_key = Gtk.Label("Podaj nazwisko panieńskie matki: ",name="white_label")
        label_auth_key.set_halign(2)
        self.entry_auth_key = Gtk.Entry()
        self.entry_auth_key.set_max_length(32)
        self.entry_auth_key.set_hexpand(False)
        self.entry_auth_key.set_vexpand(False)
        self.entry_auth_key.set_text("")  
            
        
        vertical_labels_box.pack_start(label_old_haslo, True, True, 0)
        vertical_labels_box.pack_start(label_haslo, True, True, 0)
        vertical_labels_box.pack_start(label_second_password, True, True, 0)
        vertical_labels_box.pack_start(label_auth_key, True, True, 0)
        #vertical_labels_box.set_valign(3)
            
        vertical_entries_box.pack_start(self.old_entry_password, True, True, 0)
        vertical_entries_box.pack_start(self.entry_password, True, True, 0)
        vertical_entries_box.pack_start(self.entry_second_password, True, True, 0)
        vertical_entries_box.pack_start(self.entry_auth_key, True, True, 0)
        #vertical_entries_box.set_valign(3)
            
        horizontal_box = Gtk.Box(spacing=6)
        horizontal_box.set_halign(3)
        horizontal_box.pack_start(vertical_labels_box, True, True, 0)
        horizontal_box.pack_start(vertical_entries_box, True, True, 0)


        label_main.set_hexpand(True)
        vertical_interface_box.pack_start(label_main, True, True, 0)
            
        vertical_interface_box.pack_start(horizontal_box, True, True, 0)
        vertical_interface_box.set_valign(3)
        horizontal_button_box = Gtk.Box(spacing=6)
        horizontal_button_box.set_halign(3)

        self.register_button = Gtk.Button(label="Zmień hasło",name="button_one")
        self.register_button.connect("clicked", self.Click_reset_password)
        self.register_button.set_halign(3)
        self.register_button.set_hexpand(True)

        self.back_to_login_button = Gtk.Button(label="Powrót",name="button_one")
        self.back_to_login_button.connect("clicked", self.Close_reset)
        self.back_to_login_button.set_halign(3)
        self.back_to_login_button.set_hexpand(True)

        horizontal_button_box.pack_start(self.register_button,False,True,0)
        horizontal_button_box.pack_start(self.back_to_login_button,False,True,0)
        vertical_interface_box.pack_start(horizontal_button_box, False, True, 0)
        self.window4.add(vertical_interface_box)
        self.window4.show_all()

    def Click_reset_password(self, button): 
        #jeśli jakiś błąd
        #self.Show_alert_window("tekst_bledu")

        if (self.old_entry_password.get_text() == self.entry_password.get_text()):
            alert = Alert_Window.Show_alert_window("Nowe haslo nie może być takie samo jak stare.")
            #self.Show_alert_window("Nowe haslo nie może być takie samo jak stare.")
        elif(self.entry_password.get_text() != self.entry_second_password.get_text()):
            alert = Alert_Window.Show_alert_window("Błędnie powtórzono hasło.")
            #self.Show_alert_window("Błędnie powtórzono hasło.")
        elif(len(self.entry_password.get_text())<8):
            Alert_Window.Show_alert_window("Nowe hasło jest za krótkie.")
        else:
            print("Zmiana hasła")
            global login
            #Dodać zmianę hasła
            data = req.change_password(login,self.old_entry_password.get_text(),self.entry_password.get_text(),self.entry_auth_key.get_text())
            print(data)
            c.send(data)

            time.sleep(0.4)
            if resp.accept:
                Alert_Window.Show_alert_window("Twoje hasło zostało zmienione.")
                self.window4.destroy()
            else:
                Alert_Window.Show_alert_window("Bledna odpowiedz autoryzacyjna lub obecne haslo.")

    def Close_reset(self,button):
        print("a")
        
        self.window4.destroy()

        
    def add_contact(self,nazwa):
        

        print("AAA")
        self.buttons.append(Gtk.Button(label=nazwa,xalign=0,name="button_contact"))
        self.buttons[-1].connect("clicked", self.click_contact)
        self.czat._append_user(nazwa)

        self.grid_contact.add(self.buttons[-1])
        self.scrolled_kontakty.add(self.grid_contact)

        self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        self.kontakty.show_all()
    
    def add_message(self,wiad, od):
        
        self.czat._append_msg(od, wiad)
        if(wiad[1]==1):
            label = Gtk.Label(wiad[0],name="message_come")
            label.set_line_wrap(True)
            #label.set_lines(-1)
            #label.set_max_width_chars(15)
            #label.set_alignment(0,0)
            label.set_halign(True)
            label.set_valign(True)
            label.set_size_request(10,-1)
            
                
        else:
            label = Gtk.Label(wiad[0],name="message_out")
            label.set_line_wrap(True)
            #label.set_lines(-1)
            #label.set_max_width_chars(15)
            #label.set_alignment(1,0)  #nie przesuwa w prawo
            #label.set_xalign (1.0)
            #label.set_valign(3)
            label.set_halign(2)
            label.set_valign(True)
            #label.set_halign(True)
            label.set_size_request(10,-1)
            
            return label
        return Gtk.Label("")

    def add_messages(self):   
        self.lista_wiadomosci = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10,name="message_list")
        self.lista_wiadomosci.set_size_request(600,100)
        
        self.lista_wiadomosci.set_vexpand(False)
        #self.lista_wiadomosci.set_homogeneous(True)
        #self.lista_wiadomosci.fill(True)
        #self.lista_wiadomosci.set_valign(3)

        print("zmiana czatu ", self.uzytkownik)
        messages = []
        if(self.uzytkownik!=""):
            for message in self.czat._get_msg(self.uzytkownik):
                messages.append(message) 
                
            if(len(messages)>0):
                print(messages[-1])
                for message in messages:
                    if(message[1]==1):
                        label = Gtk.Label(message[0],name="message_come")
                        label.set_line_wrap(True)
                        #label.set_lines(-1)
                        #label.set_max_width_chars(15)
                        #label.set_alignment(0,0)
                        #label.set_vexpand(False)
                        label.set_valign(True)
                        label.set_halign(True)
                        label.set_size_request(10,-1)
                        
                        self.lista_wiadomosci.pack_start(label, True, True, 0)
                    else:
                        label = Gtk.Label(message[0],name="message_out")
                        label.set_line_wrap(True)
                        #label.set_lines(-1)
                        #label.set_max_width_chars(15)
                        #label.set_alignment(1,0)  #nie przesuwa w prawo
                        #label.set_valign(3)
                        #label.set_xalign (1.0) #0.0 nie działa, 1.0 też nie
                        label.set_halign(2)
                        #label.set_vexpand(False)
                        label.set_valign(True) #nie rozciąga w górę
                        #label.set_halign(True) #nie rozciąga w bok
                        label.set_size_request(10,-1)
                        self.lista_wiadomosci.pack_start(label, True, True, 0)
                
        self.lista_wiadomosci.set_halign(3)
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size()+20)
        return self.lista_wiadomosci

    def click_delete_contact(self, button):
        self.window3 = Gtk.Window()
        self.window3.set_default_size(400, 170)
        self.window3.set_position(Gtk.WindowPosition.CENTER)
       
        label_delete = Gtk.Label("Podaj nazwę użytkownika:",name="white_label")
        self.entry_user = Gtk.Entry()
        self.entry_user.set_max_length(32)
        self.entry_user.set_hexpand(False)
        self.entry_user.set_vexpand(False)
        self.entry_user.set_text("")  

        self.button_del = Gtk.Button("Usuń",name="button_one")

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
        #jeśli jakiś błąd
        #self.Show_alert_window(tekst_bledu)

        print(self.entry_user.get_text())
        global login
        data = req.del_contact(login, self.entry_user.get_text())
        c.send(data)
        time.sleep(0.3)
        if resp.accept:
            Alert_Window.Show_alert_window("Usunięto kontakt.")
            self.window3.destroy() 
        else:
            Alert_Window.Show_alert_window("Wybrany kontakt nie istnieje.")
        #Tu dodać nazwę użytkownika do znajomych     

    def click_add_contact(self, button):
        self.window2 = Gtk.Window()
        self.window2.set_default_size(400, 170)
        self.window2.set_position(Gtk.WindowPosition.CENTER)
       
        label_add = Gtk.Label("Podaj nazwę użytkownika:",name="white_label")
        self.entry_user = Gtk.Entry()
        self.entry_user.set_max_length(32)
        self.entry_user.set_hexpand(False)
        self.entry_user.set_vexpand(False)
        self.entry_user.set_text("")  

        self.button_ok = Gtk.Button("Dodaj",name="button_one")

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
        #jeśli jakiś błąd
        #self.Show_alert_window(tekst_bledu)

        print(self.entry_user.get_text())
        global login
        data = req.add_contact(login, self.entry_user.get_text())
        c.send(data)
        time.sleep(0.4)
        if resp.accept:
            Alert_Window.Show_alert_window("Dodano kontakt.")
            #global_functions.contact_user_list += self.entry_user.get_text()
            
            self.window2.destroy()
        else: 
            Alert_Window.Show_alert_window("Brak użytkownika o podanym loginie lub jest on niedostępny.")
        #Tu dodać nazwę użytkownika do znajomych 
          

    def click_contact(self,button):
        global new_mess_info
        self.scrolled_window.remove(self.scrolled_window.get_child())
        self.uzytkownik = button.get_label()

        self.chat_name.set_text(self.uzytkownik)
        self.scrolled_window.add(self.add_messages())
        print(button.get_label())
        #butt = Gtk.Button()
        #butt.get_style_context().add_class("suggested-action")
        print(button.get_css_name())
        button.set_name("button_contact")
        button.get_style_context().remove_class("suggested-action")
        #if new_mess_info:
            #button.get_style_context().remove_class("suggested-action")
            #new_mess_info = False
        self.scrolled_window.show_all()

    def send_click(self, button):
        global income_messages_list
        wiadomosc = self.entry_wysylanie.get_text()
        #print(wiadomosc)

        if self.uzytkownik == "":
            #alert = Alert_Window.Show_alert_choose_window("Nie wybrano adresata wiadomości.")
            #self.alert.Show_alert_window()
            Alert_Window.Show_alert_window("Nie wybrano adresata wiadomości.")
        else:
            c.send(req.message(self.uzytkownik,c.login,wiadomosc))

            t = time.localtime()
            wiadomosc = main_split(self.entry_wysylanie.get_text())
            global_functions.income_messages_list.append([str(time.strftime("%H:%M:%S", t) + "\nTy:\n" + wiadomosc),2])
            self.lista_wiadomosci.pack_start(self.add_message([str(time.strftime("%H:%M:%S", t) + "\nTy:\n" + wiadomosc),2], self.uzytkownik), True, False, 1)
            self.entry_wysylanie.set_text("")
            self.entry_wysylanie.show_all()
            #self.scrolled_window.show_all()
            

            #ŁUKASZ
            #wysyłanie wiadomości
            

            adj = self.scrolled_window.get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size()) #nie pokazuje ostatniej liniki 
            #samo get_upper lub get_page_size też działa (chyba)
            #-20 sprawia że nie pokazuje też przedostatniej ale +20 nic nie zmienia
            self.scrolled_window.show_all()

    #Łukasz
    def refresh_chat(self, mess, od):
        #print(mess)
        if od not in global_functions.contact_user_list:
            al = "ADMINISTRACJA: Użytkownik " + od + " próbuje się z Tobą skontaktować. Dodaj go do listy kontaktów, aby móc z nim rozmawiać."
            #alert = Alert_Window.Show_alert_window(al)
            #pass
            global inne
            if not inne:
                self.refresh_contact_list("Inne")
                inne = True
            self.lista_wiadomosci.pack_start(self.add_message([al,1], "Inne"), True, False, 0)
            adj = self.scrolled_window.get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size()+20)
            c.send(req.message(od, c.login, "ADMINISTRACJA: Twoja wiadomość nie zostanie dostarczona ponieważ użytkownik "+ c.login + " nie dodał Cię do swojej listy kontaktów. Poinformujemy go o tym niezwłocznie."))
        else:
            self.lista_wiadomosci.pack_start(self.add_message(mess, od), True, False, 1)
            adj = self.scrolled_window.get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size()+20)
            if od == self.uzytkownik:
                print("ten sam czat")
                self.scrolled_window.remove(self.scrolled_window.get_child())
                self.scrolled_window.add(self.add_messages())
                self.scrolled_window.show_all()
                adj = self.scrolled_window.get_vadjustment()
                adj.set_value(adj.get_upper() - adj.get_page_size()+20)
            else:
                self.refresh_new_message(od)
                adj = self.scrolled_window.get_vadjustment()
                adj.set_value(adj.get_upper() - adj.get_page_size()+20)
                #Alert_Window.Show_alert_window("Użytkownik "+ od + " wysłał Ci wiadomość, by ją odczytać otwórz odpowiednie okno konwersacji.")


    def active_users(self):
       
        for user in global_functions.active_user_list:
            self.buttons.append(Gtk.Button(label=user,xalign=0,name="button_contact"))
            self.buttons[-1].connect("clicked", self.click_contact)
            self.czat._append_user(user)

        self.grid_contact.add(self.buttons[0])
        for previous_button, button in zip(self.buttons,self.buttons[1:]):
            self.grid_contact.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
        
        #Dodanie wiadmowsci
        #self.scrolled_kontakty.add(self.grid_contact)

        #self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        print("ahoj")
        self.kontakty.show_all()



    def refresh_contact_list(self,nazwa):
        #self.grid_contact = Gtk.Grid()
        #self.buttons = [] 
            
        self.buttons.append(Gtk.Button(label=nazwa,xalign=0,name="button_contact"))
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
        #self.scrolled_kontakty.add(self.grid_contact)
        #self.scrolled_kontakty.show_all()
        #self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        self.kontakty.show_all()

    def refresh_contact_list_out(self,nazwa):
        #self.grid_contact = Gtk.Grid()
        #self.buttons = [] 
        print("USUNIETO ",nazwa)
        to_del = None
        for button in self.buttons:
            if(button.get_label() == nazwa):
                to_del = button
                break
        self.grid_contact.remove(to_del)
        self.buttons.remove(to_del)
        print(len(self.buttons))
        #global_functions.active_user_list.remove(nazwa)
        #self.buttons[-1].connect("clicked", self.click_contact)
        
        '''    
        self.scrolled_kontakty = Gtk.ScrolledWindow()
        self.scrolled_kontakty.set_size_request(100,100)
        self.scrolled_kontakty.set_max_content_width(50) 

        self.scrolled_kontakty.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        '''
        #Dodanie wiadmowsci
        #self.scrolled_kontakty.add(self.grid_contact)
        #self.scrolled_kontakty.show_all()

        #HERE
        #self.kontakty.pack_start(self.scrolled_kontakty, True, True, 0)
        self.kontakty.show_all()

    def refresh_new_message(self,nazwa):
        #self.grid_contact = Gtk.Grid()
        #self.buttons = [] 
        global new_mess_info
        to_del = None
        for button in self.buttons:
            if(button.get_label() == nazwa):
                
                to_del = button                
                #to_del.background = #red
                to_del.set_name("alert_button")
                to_del = button.get_style_context().add_class("suggested-action")
                new_mess_info = True
                print("color change ", new_mess_info)
                break

        self.kontakty.show_all()

    #Lista kontaktów
    def contact_list(self):
        grid = Gtk.Grid()
        self.add(grid)
        
        buttons = [] 
        
        #Dla każdego kontaktu z listy tworzy podpisany przycisk
        for user in global_functions.active_user_list:
            buttons.append(Gtk.Button(label=user,name="button_contact"))
            self.buttons[-1].connect("clicked", self.click_contact)
            self.czat._append_user(user)

        grid.add(buttons[0])
        for previous_button, button in zip(buttons,buttons[1:]):
            grid.attach_next_to(button, previous_button, Gtk.PositionType.BOTTOM, 1, 1)
        
        return grid

    def Click_ok(self, button):
        self.wrong_data_window.destroy()   


class Alert_Window(Gtk.Grid):
    
    def __init__(self):
       
        super().__init__()
        #self.__parent_window = parent_window
        #self.connect("destroy", Gtk.main_quit)
        
        #self.Show_alert_window(tekst)
        
        
    def Show_alert_window(alert_text):
        wrong_data_window = Gtk.Window()
        wrong_data_window.set_default_size(400, 100)
        wrong_data_window.set_position(Gtk.WindowPosition.CENTER)
        
        label_wrong_data = Gtk.Label(alert_text,name="white_label")
        wrong_data_box = Gtk.VBox()
        wrong_data_box.pack_start(label_wrong_data,True,True, 1)
        
        
        wrong_data_window.add(wrong_data_box)
        wrong_data_window.show_all() 
        

    def Show_alert_choose_window(alert_text):
        wrong_data_window = Gtk.Window()
        wrong_data_window.set_default_size(400, 100)
        wrong_data_window.set_position(Gtk.WindowPosition.CENTER)
        
        label_wrong_data = Gtk.Label(alert_text)
        wrong_data_box = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL)
        wrong_data_box.pack_start(label_wrong_data,True,True, 1)

        yes = Gtk.Button("Tak",name="button_one")
        no = Gtk.Button("Nie",name="button_one")
        button_box = Gtk.VBox(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.pack_start(yes,False,True,1)
        button_box.pack_start(no,False,True,1)
        button_box.set_halign(3)
        wrong_data_box.pack_start(button_box,False,True, 1)

        
        wrong_data_window.add(wrong_data_box)
        wrong_data_window.show_all()     