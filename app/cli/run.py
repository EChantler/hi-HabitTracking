import json
import time
from fastapi.encoders import jsonable_encoder
import questionary
from app.cli.utils.process_utils import ProcessManager
import requests
import asyncio
from app.core.dtos.user import UserRequest, UserResponse
api_key = ""
base_url = "http://localhost:3434"
def auth_header(api_key: str):
    return {
    'accept': 'application/json',
    'x-key': api_key
}
def request_get(path: str, api_key: str):
    return requests.get(base_url + path, headers = auth_header(api_key))
def request_register(user: UserRequest) -> UserResponse:
    response = requests.post(base_url + "/users", json = jsonable_encoder(user))
    return UserResponse(**response.json())

def cli_app():
    print("hello")
    api_key = api_key_flow()

    return
    exit = False
    api_key = None
    hi = False
    while not exit:
        if(not hi):
            hi = questionary.text("Say 'hi' to begin.").ask() == "hi"
        else:
            print("hi. Hope you're having a lovely day!")
            if(api_key == None):
                api_key = api_key_flow()
            
            action = questionary.select(
                "What would you like to do?",
                choices=["Log a habit", "Change a habit",
                         "Marvel at your own brilliance", 
                         "Just hang around for a bit", 
                         "Be an awesome force of nature somewhere else"]).ask()
            if(action == "Log a habit"):
                log_habit()
            elif(action == "Add or change a habit"):
                pass
            elif(action == "Marvel at your own brilliance"):
                pass
            elif(action == "Just hang around for a bit"):
                questionary.text("Ok. Let's hang around for a bit. Pick a number... Any number...").ask()
                print("Awesome. I'm sure you picked a great number!")
            elif(action == "Be an awesome force of nature somewhere else"):
                exit = True

        time.sleep(1)
        if(exit):
            ProcessManager.terminate_processes()
            print("Goodbye! You can press Ctrl+C to exit.")

def log_habit():
    pass
def api_key_flow() -> str:
    print("Locating Api Key...")
    try:
        with open('token.txt', 'r') as file:
            api_key = file.read()
            print(f"Found Api Key. Testing it now...")
            response = request_get("/users", api_key)
            if(response.status_code != 200):
                print("Invalid api key")
                raise FileNotFoundError
            print("Api key valid. Using it.")
            return api_key   
    except FileNotFoundError:

        while True:
            has_token = questionary.select("I don't have a valid API key for you. How would you like to proceed?", 
                                        choices=["I have a token", "I don't have a token"]).ask()
            if(has_token == "I have a token"):
                token = questionary.text("What is your token?").ask()
                # check if the token is valid by doing an api-call
                response = request_get("/users", token)
                if(response.status_code != 200):
                    print("Invalid token. Try again.")
                    continue

                print("Token valid. Using it.")
                with open('token.txt', 'w') as file:
                    file.write(token)
                return token
            else:
                name = questionary.text("Not a problem. Let's create an account for you.\tWhat is your name?").ask()
                email = questionary.text("Great! What is your email?").ask()
                print("Awesome. Please wait while I create your account.")
                print("...")
                
                user = request_register(UserRequest(name = name, email = email))
                print(user)
                with open('token.txt', 'w') as file:
                    file.write(user.api_key)
                
                has_valid_api_key = True
                return user.api_key
                
        
    return
    try:
        with open('token.txt', 'r') as file:
            content = file.read()
            response = request_get("/user", token)
            if(response.status_code == 401):
                raise 

            return content      
    except FileNotFoundError:
        has_token = questionary.confirm("Token not found. Do you have a token?").ask()
        if(has_token):
            token = questionary.text("What is your token?").ask()
            # check if the token is valid by doing an api-call
            response = request_get("/user", token)
            
            print(response)
            #

            # store the token in a file
            with open('token.txt', 'w') as file:
                file.write(token)
            return token
        else:
            name = questionary.text("Not a problem. Let's create an account for you.\tWhat is your name?").ask()
            email = questionary.text("Great! What is your email?").ask()
            print("Awesome. Please wait while I create your account.")
            print("...")
            # create account using api
            token = "12345"
            #

            # store the token in a file
            with open('token.txt', 'w') as file:
                file.write(token)
            print("Done. You are now officially part of the community.")
            print("Your credentials have been saved locally. You can backup your token in the token.txt file.")
            return token

if __name__ == "__main__":
    cli_app()