#from kivy.app import App
#from kivy.factory import Factory
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.config import Config ,ConfigParser
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.camera import Camera 

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior,ThemeManager
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.icon_definitions import md_icons
#from kivymd.theming import ThemeManager
#from cv2 import VideoCapture ,flip
import cv2 

class backside():
    #def __init__(self,flipmode=False):
    #    self.flipmode=flipmode
    flipmode=False

    def process_frame(self,frame):
        # Process frame with opencv
        if self.flipmode :
            out=cv2.flip(frame,0).tostring()
        else:
            out=cv2.flip(frame,1).tostring()
        return out

class CvCamera(Camera):
    def __init__(self,**kwargs):
        self.flipmode=1
        super(CvCamera, self).__init__(**kwargs)
        
    def _camera_loaded(self, *largs):
        if kivy.platform=='android':
            self.texture = Texture.create(size=self.resolution,colorfmt='bgr')
            self.texture_size = list(self.texture.size)
        else:
            super(CvCamera, self)._camera_loaded()

    def on_tex(self, *l):
        if kivy.platform=='android':
            buf = self._camera.grab_frame()
            if not buf:
                return
            frame = self._camera.decode_frame(buf)
            #buf = self.process_frame(frame)
            buf=backside.process_frame(frame)
            self.texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        super(CvCamera, self).on_tex(*l)

class HomeScreen(Screen):
    
    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self._on_enter_trig = trig = Clock.create_trigger(self._my_on_enter)
        self.bind(on_enter=trig)
        
    
    def stack(self,instance):
        print(instance.icon)
        if instance.icon=="camera-iris":
            self.ids["camera"].play=not self.ids["camera"].play
        elif(instance.icon=='rotate-right-variant'):
           backside.flipmode = not backside.flipmode
           print(backside.flipmode)
        elif(instance.icon=='rotate-3d-variant'):
            try:
                self.ids["camera"].index=not self.ids["camera"].index
            except:
                self.ids["camera"].index = 0

    def _my_on_enter(self, *largs):
        pass

class SettingsScreen(Screen):
    def __init__(self,**kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        
        self._on_enter_trig = trig = Clock.create_trigger(self._my_on_enter)
        self.bind(on_enter=trig)
        
    def _my_on_enter(self, *largs):      
        pass

class MainLoop(Screen):
    pass

class MainApp(MDApp):
    def __init__(self,**kwargs):
        #self.theme_cls.theme_style="Dark"
        #self.theme_cls.theme_style="Light"        
        super().__init__(**kwargs)
    
    def on_start(self,**kwargs):
        if kivy.platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])
        
    def switch_theme_style(self,mode):
        
        if mode:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def builder(self):
        return Builder.load_file("main.kv")

if __name__=="__main__":    
    #sm=ScreenManager(WindowManager)
    #request_permissions([Permission.CAMERA])
    MainApp().run()
