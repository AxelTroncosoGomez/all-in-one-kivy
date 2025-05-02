from .basescreen import BaseScreen
from kivy.properties import ObjectProperty
from ..utils.dialogs.dialogs import show_snackbar
from kivymd.uix.toolbar import MDTopAppBar
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import NoTransition
from kivy.config import Config
from kivy.clock import Clock

class TimerScreen(BaseScreen):
    timer_finishes_sound = SoundLoader.load('src/assets/audio/bruh.wav')
    top_appbar = ObjectProperty()
    hours = ObjectProperty()
    minutes = ObjectProperty()
    seconds = ObjectProperty()
    timer = ObjectProperty()
    timer_screen_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_is_stopped = False

    def on_switch_tabs(self, *args):
        print(*args)

    def navigate_to_main(self):
        try:
            Clock.unschedule(self.inicio)
        except:
            ...
        finally:
            self.timer_screen_manager.transition = NoTransition()
            self.timer_screen_manager.current = "timer_screen_main"

    def set_timer(self):
        self.timer.text = f'{self.hours.text.zfill(2)}:{self.minutes.text.zfill(2)}:{self.seconds.text.zfill(2)}'

    def _timer_descending(self, instance):
        self.s = self.timer.text.split(':')[2]
        self.m = self.timer.text.split(':')[1]
        self.h = self.timer.text.split(':')[0]
        if int(self.h) == int(self.m):
            if int(self.s) == 1:
                show_snackbar("Timer Stoped!")
                self.timer_finishes_sound.play()
            if int(self.s) == 0:
                Clock.unschedule(self.inicio)
        if int(self.h) > 0:
            if int(self.m) == int(self.s) == 0:
                self.m = '59'
                self.s = '59'
                self.h = str(int(self.h) - 1)
                self.timer.text = f'{self.h.zfill(2)}:{self.m.zfill(2)}:{self.s.zfill(2)}'
    
        if int(self.s) > 0:
            self.s = str(int(self.s) - 1)
            self.timer.text = f'{self.h.zfill(2)}:{self.m.zfill(2)}:{self.s.zfill(2)}'

        if int(self.s) == 0 and int(self.m) > 0:
            self.s = '59'
            self.m = str(int(self.m) - 1)
            self.timer.text = f'{self.h.zfill(2)}:{self.m.zfill(2)}:{self.s.zfill(2)}'
        
    def start_timer(self):
        self.inicio = Clock.schedule_interval(self._timer_descending, 1)
        
    def resume_timer(self):
        if self.timer_is_stopped:
            self.inicio = Clock.schedule_interval(self._timer_descending, 1)

    def pause_timer(self):
        # Unschedules the timer to pause it
        try:
            Clock.unschedule(self.inicio)
            self.timer_is_stopped = True
        except Exception as e:
            show_snackbar(str(e))