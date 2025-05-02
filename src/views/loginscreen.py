from .basescreen import BaseScreen
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import NoTransition
from ..utils.dialogs.dialogs import show_snackbar

class LoginScreen(BaseScreen):
    parent_screen = ObjectProperty()
    email = ObjectProperty()
    password = ObjectProperty()

    def check_credentials(self):
        if self.email.text == "admin" and self.password.text == "admin":
            show_snackbar("Sucessfully Logged!")
            self.parent_screen.transition = NoTransition()
            self.parent_screen.current = "main_screen"
        else:
            show_snackbar("Please provide a proper username and password")