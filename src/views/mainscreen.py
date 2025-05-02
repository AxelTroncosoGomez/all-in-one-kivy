from .basescreen import BaseScreen
from kivy.properties import ObjectProperty

class MainScreen(BaseScreen):
    spendings_screen = ObjectProperty()
    home_screen = ObjectProperty()
    timer_screen = ObjectProperty()
    settings_screen = ObjectProperty()
    parent_screen = ObjectProperty()