import json
import re  # Regex or regular expression
import random_responses
import speech_recognition
import pyttsx3 as tts
import sys
import threading
import tkinter as tk
import subprocess


#from neuralintents import GenericAssistant

class Assistant:

    def __init__(self) -> None:
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate",150)

        self.root = tk.Tk()
        self.label = tk.Label(text="aa", font=("Arial", 120, "bold"))
        self.label.pack()

        self.response_data = self.load_json("/home/yuxiang/code/2023/Robotic_arm_chatbot_integration/src/bot.json")
        threading.Thread(target=self.run_assistant).start()
        self.root.mainloop()

        # Load JSON data
    def load_json(self,file):
        with open(file) as bot_responses:
            print(f"Loaded '{file}' successfully!")
            return json.load(bot_responses)

    def get_response(self,input_string, response_data):
        split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
        score_list = []

        # Check all the responses
        for response in response_data:
            response_score = 0
            required_score = 0
            required_words = response["required_words"]

            # Check if there are any required words
            if required_words:
                for word in split_message:
                    if word in required_words:
                        required_score += 1

            # Amount of required words should match the required score
            if required_score == len(required_words):
                # print(required_score == len(required_words))
                # Check each word the user has typed
                for word in split_message:
                    # If the word is in the response, add to the score
                    if word in response["user_input"]:
                        response_score += 1

            # Add score to list
            score_list.append(response_score)
            # Debugging: Find the best phrase
            # print(response_score, response["user_input"])

        # Find the best response and return it if they're not all 0
        best_response = max(score_list)
        response_index = score_list.index(best_response)

        # Check if input is empty
        if input_string == "":
            return "Please type something so we can chat :("

        # If there is no good response, return a random one.
        if best_response != 0:
            bot_output = response_data[response_index]
            if bot_output["response_type"] == "action":
                # robotic arm integration
                print("run Bash Script")
                subprocess.run(["./execute_Rviz_Python_API_Control_RoboticArm.sh"])
                
            return bot_output["bot_response"]

        return random_responses.random_string()

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:

                    # record from mic and convert from audio to text
                    self.recognizer.adjust_for_ambient_nois(mic, duration = 0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    # Hello is the trigger word, similar to whenever you say "hey Google" will wake up a Google nest
                    if "hello" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("Bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                BotResponse = self.get_response(text, self.response_data)
                                print("Bot:", BotResponse)
                                #response = self.assistant.request()
                                if BotResponse is not None:
                                    self.speaker.say(BotResponse)
                                    self.speaker.runAndWait()
                            self.label.config(fg="black")

            except Exception as error:
                print(error)
            except:
                self.label.config(fg="black")
                continue

Assistant()






