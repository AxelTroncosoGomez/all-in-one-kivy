from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

class CustomAppBar(MDTopAppBar):
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.left_action_items = [
            ["menu", lambda _: self.nav_drawer.set_state("open")]
        ]
        self.right_action_items = [
            ["dots-vertical", lambda x: self.open_right_menu(x)]
        ]
    
    def open_right_menu(self, button):
        print("Button pressed:", button)