import json
import re  # Regex or regular expression
import random_responses
import subprocess


# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

def get_response(input_string):
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
            print("----------")
            print("run Bash Script")
            subprocess.run(["./execute_Rviz_Python_API_Control_RoboticArm.sh"])
        return bot_output["bot_response"]

    return random_responses.random_string()

# Store JSON data
response_data = load_json("/home/yuxiang/code/2023/AutoPlow_NLP_ChatBot/Python_Native_Chatbot/bot.json")

while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input))
