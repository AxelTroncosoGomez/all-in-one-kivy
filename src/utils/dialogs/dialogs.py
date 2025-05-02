from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

def show_snackbar(text):
    MDSnackbar(
        MDLabel(
            text = text
        ),
        pos_hint = {"center_x": 0.5, "y": 0.01},
        radius = [30, 30, 30, 30],
        duration = 2,
        size_hint_x = 0.8
    ).open()

def confirmation_dialog(text=""):
    alert_dialog = MDDialog(
        title="Confirm Action",
        type="confirmation",
        text=text,
        buttons=[
            MDFlatButton(
                text="OK",
                on_press=lambda _: alert_dialog.dismiss()
            ),
        ],
    )
    alert_dialog.open()
