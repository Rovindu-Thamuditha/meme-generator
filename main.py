import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()

username = os.environ.get("APIUSERNAME")
password = os.environ.get("APIPASSWORD")
# Opening The meme.json file

with open("memes.json", "r") as meme_db:
    data = json.load(meme_db)

meme_list = []

for meme in data:
    id_value = meme["ID"]
    meme_name = meme["Name"]
    alt_names = meme["Alternate Names"]
    meme_list.append((id_value, meme_name))
    # print(f"ID: {id_value}")
    # print(f"Name: {meme_name}")
    # print(f"Alternate Names: {alt_names} \n ")



api_url = "https://api.imgflip.com/caption_image"

n = 1

for meme in data:
    meme_name = meme["Name"]
    print(f"{n}. {meme_name}")
    n = n + 1

print(f"{n+1}. Automeme")
selected_meme = input("Enter the number of your meme template: ")

if selected_meme.isdigit():
    selected_meme = int(selected_meme)
    if 1 <= selected_meme <= len(data):
        # Get the selected meme based on the index
        selected_index = selected_meme - 1
        selected_meme = data[selected_index]
        
        # Get the ID of the selected meme
        selected_meme_id = selected_meme["ID"]
        
        # Use the selected meme ID in your program
        print("Selected meme ID:", selected_meme_id)

        text_01 = input("Text 1: ")
        text_02 = input("Text 2: ")

        api_data = {
            "template_id" : selected_meme_id,
            "username" : username,
            "password" : password,
            "text0" : text_01,
            "text1" : text_02
        }

        api_response = requests.post(url=api_url, data=api_data)

        if api_response.status_code == 200:
            # Request was successful
            api_response = api_response.json()
            if str(api_response['success']) == "True":
                generated_meme_url = api_response['data']['url']
                decoded_url = json.loads('{"url":"' + generated_meme_url + '"}')["url"]
                print("Success")
                print(f"Meme URL : {decoded_url}")

            else:
                print("Error Occured!")
        else:
            # Request was not successful
            print("POST request failed!")
            print("Response status code:", api_response.status_code)

    elif selected_meme == n+1:
        print("Still Working on it!")
        # query_input = input("Enter your prompt for the meme :")
        # api_data = {
        #     "username" : username,
        #     "password" : password,
        #     "text" : query_input
        # }

        # api_url = "https://api.imgflip.com/automeme"
        # api_response = requests.post(url=api_url, data=api_data)

        # if api_response.status_code == 200:
        #     # Request was successful
        #     api_response = api_response.json()
        #     if str(api_response['success']) == "True":
        #         generated_meme_url = api_response['data']['url']
        #         decoded_url = json.loads('{"url":"' + generated_meme_url + '"}')["url"]
        #         print("Success")
        #         print(f"Meme URL : {decoded_url}")
        #         print("If you are not satisfied with the result try using a described prompt.")

        #     else:
        #         print("Error Occured!")
        #         print(api_response)
        # else:
        #     # Request was not successful
        #     print("POST request failed!")
        #     print("Response status code:", api_response.status_code)

    else:
        print("Invalid selection.")
else:
    print("Invalid input. Please enter a number.")
        