from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

from android.permissions import request_permissions, Permission
request_permissions([Permission.CAMERA])

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class vision(App):
    def build(self):
        layout = GridLayout(cols=2)
        left_layout=GridLayout(rows=2)
        self.cam=cv2.VideoCapture(0)
        self.frame=KivyCamera(capture=self.cam,fps=30)
        switch=Switch(active=False)
        text=Label(text="abcd")

        left_layout.add_widget(text)
        left_layout.add_widget(switch)

        layout.add_widget(self.frame)
        layout.add_widget(left_layout)
        return layout
    
    def on_stop(self):
        self.capture.release()

if __name__=="__main__":
    vision().run()