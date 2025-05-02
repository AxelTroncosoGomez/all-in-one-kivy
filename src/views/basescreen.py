from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

class BaseScreen(MDScreen):
    @property
    def root(self):
        return MDApp().get_running_app().root
    
    @property
    def app(self):
        return MDApp().get_running_app()