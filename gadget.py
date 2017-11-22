from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.utils import get_color_from_hex, get_random_color
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.graphics import Color, Rectangle, RoundedRectangle

Builder.load_string(
"""
<PanelWid>:
    #orientation: 'vertical'
    #rows: 2
    MyLab:
        id: lab_title
        size_hint_y: .3
        couleur: root.couleur
        text: root.title
        color: (1, 1, 255, 1)
        #font_size: '22sp'
        #size_hint_y: None
        #height: self.texture_size[1] + dp(10)
        #font_name: 'fonts/1942.ttf'

    MyImag:
        source: root.link
        allow_stretch: True
        keep_ratio: False

<MyLab@Label>:
    couleur: (0, 0, 0, 1)
    canvas.before:
        Color:
            rgba: self.couleur
        Rectangle:
            pos: self.pos
            size: self.size

"""
)

class PanelWid(BoxLayout):
    link = StringProperty('img/world.jpg')
    couleur = ListProperty(get_random_color())
    title = StringProperty('GanganGnoukeuDrandran')

    def __init__(self, **kw):
        super(PanelWid, self).__init__(**kw)
        self.orientation = 'vertical'
        self.rows = 2
    pass


class MyImag(ButtonBehavior, Image):
    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         print touch
    #         self.content_ = Content()
    #
    #         self.ppp = Popup(
    #             title=self.parent.ids['lab_title'].text,
    #             content=self.content_, size_hint=(.9, .7)
    #         )
    #         self.ppp.open()
    #     else:
    #         super(MyImag, self).on_touch_down(touch)

    def on_press(self):
        self.content_ = Content()
        self.ppp = Popup(
            title=self.parent.ids['lab_title'].text,
            content=self.content_, size_hint=(.5, .5)
        )
        self.ppp.open()
        #self.source = 'img/colors.png'

        #return True

class Content(BoxLayout):
    def __init__(self, **kw):
        super(Content, self).__init__(**kw)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(size=self.rect_update, pos=self.rect_update)

    def rect_update(self, *args):
        self.rect.pos = args[0].pos
        self.rect.size = args[0].size


class MyWid(App):
    def build(self):
        return PanelWid()


if __name__ == '__main__':
    MyWid().run()