from .basescreen import BaseScreen
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import NoTransition

class SettingsScreen(BaseScreen):
    top_appbar = ObjectProperty()
    settings_screen_manager = ObjectProperty()
    parent_screen = ObjectProperty()

    def on_enter(self):
        print("Entered SettingsScreen")
        print(self.parent_screen)

    def on_leave(self):
        print("Left SettingsScreen")

    def go_back(self):
        self.parent_screen.transition = NoTransition()
        self.parent_screen.current = "main_screen"