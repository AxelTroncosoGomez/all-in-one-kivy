from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty

class DrawerContent(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    top_appbar = ObjectProperty()