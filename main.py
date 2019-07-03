#Fastest Lap App take 1
#region Imports
import kivy
import logging
import numpy as np
import obd 
import cv2
import time
import pyautogui
import bluetooth
from kivy.clock import Clock
from PIL import ImageGrab
from obd import OBDStatus
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Rectangle
#endregion

#Global Car Connection. It can be changed for any children class/method
connection = obd.Async()
#Global recording variable. It changes every time User wants to finish the recording
recording = True
#Global Video Writer and output file
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter("lap.mp4",fourcc, 30, pyautogui.size())

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    def run_event(self):
        print("Begin of obd connection routine")
        def new_rpm(r):    
            self.lbl_rpm.text = r.value
        def new_speed(s):
            self.lbl_speed.text = s.value

        connection.watch(obd.commands.RPM, callback=new_rpm)
        connection.watch(obd.commands.SPEED, callback=new_speed)
        connection.start()
        time.sleep(1)
        global recording

        #This method saves the screenshots from screen until recording = false
        def selfie(self):
            if not recording:
                print("Stopped!")
                selfie_event.cancel()    
            else:
                img = ImageGrab.grab()
                img_np = np.array(img)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                out.write(frame)
                #cv2.imshow("Screen", frame)
                #print("Image grabbed")

        selfie_event = Clock.schedule_interval(selfie, 1/10)

        #cv2.destroyAllWindows()
        print("End of obd connection routine")

    def close_connection(self):
        connection.stop()
    def out_of_second_window(self):
        global recording 
        recording = False
        out.release()
        print("Stopping recording")


class ScreenManager(Screen):
    pass

kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()


logging.basicConfig(level=logging.DEBUG)
