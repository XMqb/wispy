# Version 0.0.0
# Developed by XM
# (C) 2021

# TO DO:
# Tor access
# Find domain/host
# E2EE messages
# User/pass system
# Link sharing
# Keep message history locally

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.text import FontContextManager as FCM
import WISPclient
import os
import sys
Config.set('graphics', 'resizable', False) #0 being off 1 being on as in true/false
Window.size = (500, 500)
kivy.require("1.00.0")

Builder.load_file('WiSP.kv')

class RoundedButton(Button):
    pass

class RoundedButtonTwo(Button):
    pass

class RoundedInput(TextInput):
    pass

class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols = 1, size_hint_y = None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y = None, markup = True)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, message):
        self.chat_history.text += "\n" + message

        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98, None)

        #self.scroll_to(self.scroll_to_point)
        self.scroll_to(self.chat_history)

    def update_chat_history_layout(self, _=None):
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt", "r") as f:
                d = f.read().split(":")
                previp = d[0]
                prevport = d[1]
                prevuser = d[2]
        else:
            previp = ""
            prevport = ""
            prevuser = ""

        self.add_widget(Label())
        self.img = Image(source ='wisplogo.png')
        self.img.allow_stretch = True
        self.img.keep_ratio = True
        self.img.size_hint_x = 1
        self.img.size_hint_y = None
        self.img.pos = (200, 100)
        self.img.opacity = 1
        self.add_widget(self.img)
        #self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Label(text = "IPv4:"))
        self.ip = RoundedInput(text = previp, multiline = False)
        self.add_widget(self.ip)
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Label(text = "Port:"))
        self.port = RoundedInput(text = prevport, multiline = False)
        self.add_widget(self.port)
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Label(text = "User:"))
        self.username = RoundedInput(text = prevuser, multiline = False)
        self.add_widget(self.username)
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Label(text = " "))
        self.join = RoundedButton(text = "Login")
        self.join.bind(on_press = self.join_button)
        self.add_widget(self.join)
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

    def join_button(self, instance):
        ip = self.ip.text
        port = self.port.text
        username = self.username.text
        #print(f"Attempting to join {ip}:{port} as {username}...")

        with open("prev_details.txt", "w") as f:
            f.write(f"{ip}:{port}:{username}")

        info = f"Attempting to join {ip}:{port} as {username}..."
        chat_app.infopage.update_info(info)
        chat_app.screen_manager.current = "Info"

        Clock.schedule_once(self.connect, 1)

    def connect(self, _):
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text

        if not WISPclient.connect(ip, port, username, show_error):
            return
        chat_app.create_chat_page()
        chat_app.screen_manager.current = "Chat"


class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign = "center", valign = "middle", font_size = 30)
        self.message.bind(width = self.update_text_width)
        self.add_widget(self.message)
    def update_info(self, message):
        self.message.text = message
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3

        self.history = ScrollableLabel(width = Window.size[0]*0.95, height = Window.size[1]*0.92, size_hint_y = None,size_hint_x = None)
        self.placeholderlololol = Label(width = Window.size[0]*0.01, size_hint_x = None)

        top_line = GridLayout (cols = 2, height = Window.size[1]*0.92, size_hint_y = None, width = Window.size[0]*0.95, size_hint_x = None)
        top_line.add_widget(self.placeholderlololol)
        top_line.add_widget(self.history)
        self.add_widget(top_line)

        self.borderlinelololol = Label(height = Window.size[1]*0.02, size_hint_y = None)
        self.add_widget(self.borderlinelololol)

        self.new_message = RoundedInput(width = Window.size[0]*0.5, size_hint_x = None, multiline = False)
        self.send = RoundedButtonTwo(text = "SEND", width = Window.size[0]*0.06, size_hint_x = None)
        self.send.bind(on_press = self.send_message)
        self.placeholderlololol1 = Label(width = Window.size[0]*0.03, size_hint_x = None)
        self.placeholderlololol2 = Label(width = Window.size[0]*0.06, size_hint_x = None)
        self.placeholderlololol3 = Label(width = Window.size[0]*0.01, size_hint_x = None)
        self.placeholderlololol4 = Label(width = Window.size[0]*0.04, size_hint_x = None)
        self.placeholderlololol5 = Label(width = Window.size[0]*0.03, size_hint_x = None)

        bottom_line = GridLayout(cols = 7)
        bottom_line.add_widget(self.placeholderlololol1)
        bottom_line.add_widget(self.placeholderlololol3)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.placeholderlololol2)
        bottom_line.add_widget(self.placeholderlololol4)
        bottom_line.add_widget(self.send)
        bottom_line.add_widget(self.placeholderlololol5)
        self.add_widget(bottom_line)

        Window.bind(on_key_down = self.on_key_down)

        Clock.schedule_once(self.focus_text_input, 1)
        WISPclient.start_listening(self.incoming_message, show_error)
        self.bind(size = self.adjust_fields)

    def adjust_fields(self, *_):
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.93
        self.history.height = new_height
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width
        Clock.schedule_once(self.history.update_chat_history_layout)


    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40: #enter key
            self.send_message(None)

    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ""
        if message:
            self.history.update_chat_history(f"([color=00dd99]{chat_app.connect_page.username.text}[/color]): {message}")
            WISPclient.send(message)

        Clock.schedule_once(self.focus_text_input, 0.1)

    def focus_text_input(self, _):
        self.new_message.focus = True

    def incoming_message(self, username, message):
        self.history.update_chat_history(f"([color=99dd00]{username}[/color]): {message}")


#        print("Sent a message.")
#        self.add_widget(Label(text = "lol hey there sexy"))


class WiSPApp(App):
    def build(self):
        #return Label(text = "Yo.")
        #return ConnectPage()
        self.screen_manager = ScreenManager()

        self.connect_page = ConnectPage()
        screen = Screen(name = "Connect")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.infopage = InfoPage()
        screen = Screen(name = "Info")
        screen.add_widget(self.infopage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def create_chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name = "Chat")
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)

def show_error(message):
    chat_app.infopage.update_info(message)
    chat_app.screen_manager.current = "Info"
    Clock.schedule_once(sys.exit, 3)

if __name__ == "__main__":
    chat_app = WiSPApp()
    chat_app.run()


# self.add_widget(AsyncImage(url))
# return Image(source ='download.jpg')
