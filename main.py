# -*- coding: utf8 -*-
import re
import kivy
kivy.require('1.9.0')

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition, FallOutTransition
from kivy.utils import get_color_from_hex

from kivy.garden.notification import Notification
from gadget import PanelWid
from color_dict import get_color, color_choice
from db import db


class ConnexionScreen(Screen):
    def validate(self):
        #db.table('users').get()
        if self.ids['pseudo_input'].text == '' and self.ids['pwd_input'].text == '':
            # self.ids['pseudo_input'].foreground_color = [1, 0, 0, 1]
            self.ids['pseudo_input'].text = 'Ecrivez votre nom svp!'

        else:
            email = self.ids['pseudo_input'].text
            print(email)
            try:
                user = db.table('students').where('email', email).first()
                print(user.name)
            except:
                pass

            #print(user.password)
            if user:
                if self.ids['pwd_input'].text == user['password']:
                    self.manager.current = 'home'
                    print('--------')
                    print('--------')
                    print(email)
                    print('--------')
                    print(user['name'])
                    self.ids['pseudo_input'].text = ''
                    self.ids['pwd_input'].text = ''
            # self.ids['pseudo_input'].foreground_color = 0.204, 0.286, 0.369, 1.0


    def restore_focus(self):
        Notification().open(
            title='champ vide!',
            message='Veuillez remplir le champ',
            timeout=5
        )
        # self.ids['pseudo_input'].foreground_color = 0.204, 0.286, 0.369, 1.0
        # self.ids['pseudo_input'].text = ''

    def on_enter(self, *args):
        self.ids['pseudo_input'].text = ''
        self.ids['pwd_input'].text = ''
    pass


class RegisterScreen(Screen):
    def validate(self):
        name = self.ids['name_id'].text
        email = self.ids['email_id'].text
        number = self.ids['nbr_id'].text
        pwd = self.ids['pwd_id'].text
        pwd_again = self.ids['pwda_id'].text

        nbrRegex = re.compile(
            r'\d\d-\d\d\d-\d\d\d'
        )
        match_nbr = nbrRegex.search(number)
        if match_nbr is None:
            self.ids['nbr_id'].text = 'ex: 48-O78-646'

        # print(match_nbr.group())

        if pwd != pwd_again:
            self.ids['pwda_id'].password = False
            self.ids['pwd_id'].password = False
            self.ids['pwda_id'].text = 'password doesnt match'
            self.ids['pwd_id'].text = 'password doesnt match'

        else:
            if name and email and number:
                db.table('students').insert_get_id(
                    {
                        'name': name,
                        'email': email,
                        'password': pwd_again
                    }
                )
                self.ids['name_id'].text = ''
                self.ids['email_id'].text = ''
                self.ids['nbr_id'].text = ''
                self.ids['pwd_id'].text = ''
                self.ids['pwda_id'].text = ''
                self.manager.current = 'login'


class Panel(PanelWid):
    def __init__(self, **kw):
        super(Panel, self).__init__(**kw)


class HomeScreen(Screen):

    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
        self.panel1 = Panel()
        self.panel2 = Panel()
        self.panel2.title = 'Riz couché'
        self.panel2.link = 'img/hot-air.png'
        self.panel2.couleur = color_choice['seagreen']
        self.panel3 = Panel()
        self.panel3.title = 'Sauce graine'
        self.panel3.link = 'img/adobe2.jpg'
        self.panel3.couleur = color_choice['teal']
        self.ids['grid'].add_widget(self.panel1)
        self.ids['grid'].add_widget(self.panel2)
        self.ids['grid'].add_widget(self.panel3)
    pass


class RecetteScreen(Screen):
    def __init__(self, **kw):
        super(RecetteScreen, self).__init__(**kw)
        self.ids['preparation_input'].disabled = True
    pass


class MainScreen(Screen):

    pass


def get_mgr():
    sm = ScreenManager()
    sm.transition = CardTransition(direction='up', mode='pop')
    sm.add_widget(MainScreen(name='principal'))
    sm.add_widget(ConnexionScreen(name='login'))
    sm.add_widget(RegisterScreen(name='register'))
    sm.add_widget(HomeScreen(name='home'))
    sm.add_widget(RecetteScreen(name='recette'))
    #sm.current = 'home'

    return sm


class ITCApp(App):
    icon = 'img/itc.png'
    title = 'lahlia'

    def build(self):
        ecran = get_mgr()
        return ecran


if __name__ == '__main__':
    ITCApp().run()
