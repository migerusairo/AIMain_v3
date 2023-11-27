from kivy.animation import Animation
from kivy.metrics import dp

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.utils import rgba

import json
import re
import pyaudio
import pyttsx3
import speech_recognition as sr
import requests
import pyrebase
from firebase import firebase

import Love_responses as Love

firebaseConfig = {
    'apiKey': "AIzaSyC8y4Qv-20aS701U6OeawNySy7VkrmEcEw",
    'databaseURL': "https://aiproject-db-default-rtdb.firebaseio.com/",
    'authDomain': "aiproject-db.firebaseapp.com",
    'projectId': "aiproject-db",
    'storageBucket': "aiproject-db.appspot.com",
    'messagingSenderId': "88380585609",
    'appId': "1:88380585609:web:98a89b3b32afc2b191f858",
    'measurementId': "G-ME9WFNYR6M"
}

Firebase = pyrebase.initialize_app(firebaseConfig)
auth = Firebase.auth()

firebase = firebase.FirebaseApplication('https://aiproject-db-default-rtdb.firebaseio.com/', None)

# ----------------------------------------------------------------------------------------------------------------------

Window.size = (310, 650)

# ----------------------------------------------------------------------------------------------------------------------
engine = pyttsx3.init()


# ----------------------------------------------------------------------------------------------------------------------
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages_love(message):
    highest_prob_list = {}

    def love_response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # sample---------------------------------------------------------------------------------------------------

    love_response('Hello!, How are you?', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    love_response('See you!', ['bye', 'goodbye'], single_response=True)
    love_response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    love_response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    love_response('Thank you!', ['i', 'love', 'coding'], required_words=['coding'])

    # ----------------------------------------------------------------------------------------------------------
    love_response(Love.love(), ['i', 'want', 'to', 'confess'], required_words=['want', 'confess'])
    love_response(Love.love(), ['i', 'want', 'to', 'confess'], required_words=['confess'])
    love_response(Love.love(), ['i', 'want', 'to', 'confess'], required_words=['want'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return Love.unknown() if highest_prob_list[best_match] < 1 else best_match


def check_all_messages_academic(message):
    highest_prob_list = {}

    def academic_response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    academic_response(Academic.academic(), ['academic', ], required_words=['academic, books'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return Academic.unknown() if highest_prob_list[best_match] < 1 else best_match


def check_all_messages_family(message):
    highest_prob_list = {}

    def family_response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    family_response(Family.family(), ['i', 'want', 'to', 'go'], required_words=['want', 'go'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return Family.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def love_get_response(love_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', love_input.lower())
    response = check_all_messages_love(split_message)
    return response


def academic_get_response(academic_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', academic_input.lower())
    response = check_all_messages_academic(split_message)
    return response


def family_get_response(family_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', family_input.lower())
    response = check_all_messages_academic(split_message)
    return response


class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 14


class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 14


class User_data(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "fonts/PoppinsEL.otf"
    font_size = 13


class TCUAdvisor(MDApp):
    def build(self):

        self.icon = "assets/TCULogo.jpg"

        global screen
        screen = ScreenManager(transition=SlideTransition(duration=.8))
        screen.add_widget(Builder.load_file("Introduction.kv"))
        screen.add_widget(Builder.load_file("Login.kv"))
        screen.add_widget(Builder.load_file("Register.kv"))
        screen.add_widget(Builder.load_file("Admin_login.kv"))
        screen.add_widget(Builder.load_file("Admin_Home-screen.kv"))
        screen.add_widget(Builder.load_file("Admin_Home-screen2.kv"))
        screen.add_widget(Builder.load_file("Welcome-screen.kv"))
        screen.add_widget(Builder.load_file("Home-screen.kv"))
        screen.add_widget(Builder.load_file("Notification-screen.kv"))
        screen.add_widget(Builder.load_file("Profile-screen.kv"))
        screen.add_widget(Builder.load_file("Setting-screen.kv"))
        screen.add_widget(Builder.load_file("About.kv"))
        screen.add_widget(Builder.load_file("Forgot-password.kv"))
        screen.add_widget(Builder.load_file("Love_message-screen.kv"))
        screen.add_widget(Builder.load_file("Academic_message-screen.kv"))
        screen.add_widget(Builder.load_file("Family_message-screen.kv"))
        return screen

    # Voices----------------------------------------------------------------------------------------------------------
    def speak_male(self, text):
        engine.setProperty('rate', 160)
        engine.setProperty('pitch', 100)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

        engine.say(text)
        engine.runAndWait()

    def speak_female(self, text):
        engine.setProperty('rate', 160)
        engine.setProperty('pitch', 100)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        engine.say(text)
        engine.runAndWait()

    # Command & Responses -----------------------------------------------------------------------------------

    def send_love(self):
        global size, halign, command
        if screen.get_screen('Love_message-screen').text_input != "":
            love_input = screen.get_screen('Love_message-screen').text_input.text
            if len(love_input) < 6:
                size = .22
                halign = "center"
            elif len(love_input) < 11:
                size = .32
                halign = "center"
            elif len(love_input) < 16:
                size = .45
                halign = "center"
            elif len(love_input) < 21:
                size = .58
                halign = "center"
            elif len(love_input) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Command(text=love_input, size_hint_x=size, halign=halign))

            if len(love_input) < 6:
                size = .45
                halign = "center"
            elif len(love_input) < 11:
                size = .50
                halign = "center"
            elif len(love_input) < 16:
                size = .60
                halign = "center"
            elif len(love_input) < 21:
                size = .70
                halign = "center"
            elif len(love_input) < 26:
                size = .70
                halign = "center"
            else:
                size = .70
                halign = "left"

            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Response(text=love_get_response(love_input), size_hint_x=size, halign=halign))

            screen.get_screen('Love_message-screen').text_input.text = ""

    def send_academic(self):
        global size, halign, command
        if screen.get_screen('Academic_message-screen').text_input != "":
            academic_input = screen.get_screen('Academic_message-screen').text_input.text
            if len(academic_input) < 6:
                size = .22
                halign = "center"
            elif len(academic_input) < 11:
                size = .32
                halign = "center"
            elif len(academic_input) < 16:
                size = .45
                halign = "center"
            elif len(academic_input) < 21:
                size = .58
                halign = "center"
            elif len(academic_input) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen.get_screen('Academic_message-screen').chat_list.add_widget(
                Command(text=academic_input, size_hint_x=size, halign=halign))

            if len(academic_input) < 6:
                size = .45
                halign = "center"
            elif len(academic_input) < 11:
                size = .50
                halign = "center"
            elif len(academic_input) < 16:
                size = .60
                halign = "center"
            elif len(academic_input) < 21:
                size = .70
                halign = "center"
            elif len(academic_input) < 26:
                size = .70
                halign = "center"
            else:
                size = .70
                halign = "left"

            screen.get_screen('Academic_message-screen').chat_list.add_widget(
                Response(text=academic_get_response(academic_input), size_hint_x=size, halign=halign))

            screen.get_screen('Academic_message-screen').text_input.text = ""

    def send_family(self):
        global size, halign, command
        if screen.get_screen('Family_message-screen').text_input != "":
            family_input = screen.get_screen('Family_message-screen').text_input.text
            if len(family_input) < 6:
                size = .22
                halign = "center"
            elif len(family_input) < 11:
                size = .32
                halign = "center"
            elif len(family_input) < 16:
                size = .45
                halign = "center"
            elif len(family_input) < 21:
                size = .58
                halign = "center"
            elif len(family_input) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen.get_screen('Family_message-screen').chat_list.add_widget(
                Command(text=family_input, size_hint_x=size, halign=halign))

            if len(family_input) < 6:
                size = .45
                halign = "center"
            elif len(family_input) < 11:
                size = .50
                halign = "center"
            elif len(family_input) < 16:
                size = .60
                halign = "center"
            elif len(family_input) < 21:
                size = .70
                halign = "center"
            elif len(family_input) < 26:
                size = .70
                halign = "center"
            else:
                size = .70
                halign = "left"

            screen.get_screen('Family_message-screen').chat_list.add_widget(
                Response(text=family_get_response(family_input), size_hint_x=size, halign=halign))

            screen.get_screen('Family_message-screen').text_input.text = ""

    def Love_take_command(self):

        global size, halign, command

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening . . .")
            r.pause_threshold = 1
            text = r.listen(source)
        try:
            print("Recognizing. . .")
            command = r.recognize_google(text, language='en-in')
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"

            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))

            screen.get_screen('Love_message-screen').chat_list.add_widget(
                Response(text=love_get_response(command), size_hint_x=size, halign=halign))

            self.speak_female(love_get_response(command))

            return

        except Exception as e:
            print(e)

            return "None"

    def Academic_take_command(self):

        global size, halign, command

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening . . .")
            r.pause_threshold = 1
            text = r.listen(source)
        try:
            print("Recognizing. . .")
            command = r.recognize_google(text, language='en-in')
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen.get_screen('Academic_message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))

            screen.get_screen('Academic_message-screen').chat_list.add_widget(
                Response(text=academic_get_response(command), size_hint_x=size, halign=halign))

            self.speak_female(academic_get_response(command))
            return
        except Exception as e:
            print(e)
            return "None"

    def Family_take_command(self):

        global size, halign, command

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening . . .")
            r.pause_threshold = 1
            text = r.listen(source)
        try:
            print("Recognizing. . .")
            command = r.recognize_google(text, language='en-in')
            if len(command) < 6:
                size = .22
                halign = "center"
            elif len(command) < 11:
                size = .32
                halign = "center"
            elif len(command) < 16:
                size = .45
                halign = "center"
            elif len(command) < 21:
                size = .58
                halign = "center"
            elif len(command) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            screen.get_screen('Family_message-screen').chat_list.add_widget(
                Command(text=command, size_hint_x=size, halign=halign))

            screen.get_screen('Family_message-screen').chat_list.add_widget(
                Response(text=family_get_response(command), size_hint_x=size, halign=halign))

            self.speak_female(family_get_response(command))

            return
        except Exception as e:
            print(e)
            return "None"

    # User Registration----------------------------------------------------------------------------------------------------

    def register(self, email, password, confirmpassword, fname, lname, stud_id, year, course, section):
        result = firebase.get('aiproject-db-default-rtdb/Users', '')
        for i in result.keys():
            if any(field == "" for field in
                   [email, password, confirmpassword, fname, lname, stud_id, year, course, section]):
                Snackbar(text="Please fill out all fields!",
                         snackbar_animation_dir="Top",
                         font_size='12sp',
                         snackbar_x=.1,
                         size_hint_x=.999,
                         size_hint_y=.07,
                         bg_color=(1, 0, 0, 1),
                         ).open()
                return

            if len(password) < 6:
                Snackbar(text="Weak Password!",
                         snackbar_animation_dir="Top",
                         font_size='12sp',
                         snackbar_x=.1,
                         size_hint_x=.999,
                         size_hint_y=.07,
                         bg_color=(1, 0, 0, 1)
                         ).open()

            if stud_id == result[i]['Student ID']:
                Snackbar(text="Student ID already used!",
                         snackbar_animation_dir="Top",
                         font_size='12sp',
                         snackbar_x=.1,
                         size_hint_x=.999,
                         size_hint_y=.07,
                         bg_color=(1, 0, 0, 1)
                         ).open()

            else:
                try:
                    if password == confirmpassword:
                        screen = self.root.get_screen('Register')
                        if screen.ids.checkbox.active:
                            auth.create_user_with_email_and_password(email, password)
                            Snackbar(text="Registered Successfully!",
                                     snackbar_animation_dir="Top",
                                     font_size='12sp',
                                     snackbar_x=.1,
                                     size_hint_x=.999,
                                     size_hint_y=.07,
                                     bg_color="#000000"
                                     ).open()

                            data = {
                                'First Name': fname,
                                'Last Name': lname,
                                'Student ID': stud_id,
                                'Year': year,
                                'Course': course,
                                'Section': section,
                                'Email': email,
                                'Password': password
                            }

                            firebase.post('aiproject-db-default-rtdb/Users', data)
                            self.clear_registration_fields()
                            self.root.current = 'Login'
                        else:
                            Snackbar(text="Accept terms & Condition!",
                                     snackbar_animation_dir="Top",
                                     font_size='12sp',
                                     snackbar_x=.1,
                                     size_hint_x=.999,
                                     size_hint_y=.07,
                                     bg_color=(1, 0, 0, 1)
                                     ).open()
                    else:
                        Snackbar(text="Invalid Confirm Password!",
                                 snackbar_animation_dir="Top",
                                 font_size='12sp',
                                 snackbar_x=.1,
                                 size_hint_x=.999,
                                 size_hint_y=.07,
                                 bg_color=(1, 0, 0, 1)
                                 ).open()

                except:
                    Snackbar(text="Email already existed!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1)
                             ).open()

    # Admin & User Login----------------------------------------------------------------------------------------------------
    def user_login(self, email, password):
        try:
            auth.sign_in_with_email_and_password(email, password)

            self.root.current = 'Welcome-screen'
            self.carousel_autonext()
            self.clear_user_login_fields()

            result = firebase.get('aiproject-db-default-rtdb/Users', '')
            for i in result.keys():

                if email == result[i]['Email']:
                    screen.get_screen('Setting-screen').add_widget(
                        User_data(text=result[i]['First Name'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': 0.76, 'center_y': 0.87}))
                    screen.get_screen('Setting-screen').add_widget(
                        User_data(text=result[i]['Last Name'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': 1.03, 'center_y': 0.87}))

                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=result[i]['First Name'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': .75, 'center_y': 0.61}))

                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=result[i]['Student ID'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': .75, 'center_y': 0.51}))

                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=result[i]['Year'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': .75, 'center_y': 0.41}))

                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=result[i]['Course'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': .95, 'center_y': 0.41}))

                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=result[i]['Section'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': .75, 'center_y': 0.31}))

                    screen.get_screen('Profile-screen').add_widget(
                        User_data(text=result[i]['Last Name'], font_name="fonts/OpenSans-Semibold.ttf",
                                  pos_hint={'center_x': .75, 'center_y': 0.61}))

                    return

        except:
            Snackbar(text="Invalid Email or Password!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1)
                     ).open()
            return

    def admin_login(self, admin_id, admin_password):
        result = firebase.get('aiproject-db-default-rtdb/Admin', '')
        for i in result.keys():
            if result[i]['Admin ID'] == admin_id:
                if result[i]['Admin Password'] == admin_password:
                    Snackbar(text="Logged In!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color="#000000"
                             ).open()
                    self.display_all_user()
                    self.root.current = 'Adminhome'
                    self.clear_admin_login_fields()
                    return

        for i in result.keys():
            if result[i]['Admin ID'] == admin_id:
                if result[i]['Admin Password'] != admin_password:
                    Snackbar(text="Invalid ID or Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1)
                             ).open()
                    return

        for i in result.keys():
            if result[i]['Admin ID'] != admin_id:
                if result[i]['Admin Password'] == admin_password:
                    Snackbar(text="Invalid ID or Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1)
                             ).open()
                    return

        for i in result.keys():
            if result[i]['Admin ID'] != admin_id:
                if result[i]['Admin Password'] != admin_password:
                    Snackbar(text="Invalid ID or Password!",
                             snackbar_animation_dir="Top",
                             font_size='12sp',
                             snackbar_x=.1,
                             size_hint_x=.999,
                             size_hint_y=.07,
                             bg_color=(1, 0, 0, 1)
                             ).open()
                    return

    # Clearing Inputs-------------------------------------------------------------------------------------------------------
    def clear_registration_fields(self):
        screen = self.root.get_screen('Register')
        screen.ids.stud_id.text = ""
        screen.ids.fname.text = ""
        screen.ids.lname.text = ""
        screen.ids.year.text = ""
        screen.ids.course.text = ""
        screen.ids.section.text = ""
        screen.ids.email.text = ""
        screen.ids.password.text = ""
        screen.ids.confirmpassword.text = ""

    def clear_admin_login_fields(self):
        screen = self.root.get_screen('Admin_login')
        screen.ids.admin_id.text = ""
        screen.ids.admin_password.text = ""

    def clear_user_login_fields(self):
        screen = self.root.get_screen('Login')
        screen.ids.email.text = ""
        screen.ids.password.text = ""

    # Admin & User Logout---------------------------------------------------------------------------------------------------

    def user_logout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()

        self.root.current = 'Login'

    def admin_logout(self):
        Snackbar(text="Logged out successful!",
                 snackbar_animation_dir="Top",
                 font_size='12sp',
                 snackbar_x=.1,
                 size_hint_x=.999,
                 size_hint_y=.07,
                 bg_color=(1, 0, 0, 1)
                 ).open()
        self.root.current = 'Admin_login'

    # Display Users profile & Admin Homescreen users---------------------------------------------------------------------------------------------------------------
    def display_all_user(self):
        result = firebase.get('aiproject-db-default-rtdb/Users', '')
        for i in result.keys():
            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Name:               " + result[i]['First Name'] + "" + result[i]['Last Name'],
                          font_name="fonts/OpenSans-Bold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}, font_size=14))

            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Student ID:            " + result[i]['Student ID'],
                          font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Year & Course:     " + result[i]['Year'] + " - " + result[i]['Course'],
                          font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Section:                   " + result[i]['Section'],
                          font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="Email:                      " + result[i]['Email'],
                          font_name="fonts/OpenSans-Semibold.ttf",
                          pos_hint={"center_x": .6, "center_y": .5}))

            screen.get_screen('Adminhome').user_list.add_widget(
                User_data(text="---------------------------------------------------", opacity=.5))

    # other functions--------------------------------------------------------------------------------------------------
    def carousel_autonext(self):
        screen = self.root.get_screen('Home-screen')
        carousel_1 = screen.ids.carousel_1
        carousel_1.loop = True
        Clock.schedule_interval(carousel_1.load_next, 3)

        screen = self.root.get_screen('Home-screen')
        carousel_2 = screen.ids.carousel_2
        carousel_2.loop = True
        Clock.schedule_interval(carousel_2.load_next, 3)

        screen = self.root.get_screen('Welcome-screen')
        carousel = screen.ids.carousel
        Clock.schedule_interval(carousel.load_next, 7)

    def current_slide(self, index):
        screen = self.root.get_screen('Welcome-screen')
        for i in range(2):
            if index == i:
                screen.ids[f"slide{index}"].color = rgba(255, 0, 0, 255)
            else:
                screen.ids[f"slide{i}"].color = rgba(170, 170, 170, 255)

        screen = self.root.get_screen('Register')
        for i in range(2):
            if index == i:
                screen.ids[f"slide{index}"].color = rgba(255, 0, 0, 255)
            else:
                screen.ids[f"slide{i}"].color = rgba(170, 170, 170, 255)

    def terms_condition(self):
        show = MDLabel(text="Please read these terms and conditions", font_name="fonts/OpenSans-Semibold.ttf",
                       pos_hint={"center_x": 1, "center_y": .5})

        popupWindow = Popup(title="Terms & Conditions", title_color="black",
                            title_font="fonts/OpenSans-Bold.ttf",
                            separator_color=[160 / 255., 160 / 255., 160 / 255., 1.], content=show,
                            size_hint=(None, None), size=(300, 400), background="white")
        popupWindow.open()

    def reset_password(self, email):
        try:
            auth.send_password_reset_email(email)
            dialog = MDDialog(title="Email Verification", text="Please check your email address.", pos_hint={"center_x": .5, "center_y": .85})
            dialog.open()
            self.root.current = 'Login'
        except:
            Snackbar(text="Invalid Email!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1)
                     ).open()

    def is_cnx_active(self, timeout):
        try:
            requests.head("https://www.google.com/", timeout=timeout)
            print("The internet connection is active")
        except requests.ConnectionError:
            Snackbar(text="Please Check your Internet connection!",
                     snackbar_animation_dir="Top",
                     font_size='12sp',
                     snackbar_x=.1,
                     size_hint_x=.999,
                     size_hint_y=.07,
                     bg_color=(1, 0, 0, 1)
                     ).open()

    def on_touch(self, instance):
        pass

    def on_start(self):
        Clock.schedule_once(self.start, 3)

    def start(self, *args):
        self.root.current = "Login"
        self.is_cnx_active(1)

if __name__ == "__main__":
    TCUAdvisor().run()

# ----------------------------------------------------
# def next(self):
#     screen = self.root.get_screen('Welcome-screen')
#     carousel = screen.ids.carousel
#     carousel.load_next(mode="next")

# -----------------------------------------------------
# screen = self.root.get_screen('About')
# bg_image = screen.ids.bg_image
# Animation(x=-dp(300), d=30).start(bg_image)
