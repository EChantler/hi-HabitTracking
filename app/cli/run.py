import json
import time
from fastapi.encoders import jsonable_encoder
import questionary
from app.cli.utils.process_utils import ProcessManager
import requests
import asyncio
from app.core.dtos.habit import HabitResponse
from app.core.dtos.habit_entry import HabitEntryRequest
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
def habits_get(api_key: str) -> list[HabitResponse]:
    response =requests.get(base_url + "/habits", headers = auth_header(api_key))
    return response.json()
def habits_create(api_key: str, name: str, periodicity: int, completion_criteria: int):
    requests.post(base_url + "/habits", json = {"name": name, "periodicity": periodicity, "completion_criteria": completion_criteria}, headers = auth_header(api_key))
def habit_entry(api_key: str, habit_id: int):
    requests.post(base_url + "/habit-entries", json = jsonable_encoder(HabitEntryRequest(habit_id = habit_id)), headers = auth_header(api_key))
def habits_change(api_key: str, habit_id: int ,name: str, periodicity: int, completion_criteria: int):
    requests.put(base_url + "/habits/"+ str(habit_id), json = {"name": name, "periodicity": periodicity, "completion_criteria": completion_criteria}, headers = auth_header(api_key))
def habit_delete(api_key: str, habit_id: int):
    requests.delete(base_url + "/habits/" + str(habit_id), headers = auth_header(api_key))
def cli_app():
    
    api_key = api_key_flow()
    hi = False
    exit = False
    first_greet = True
    while not exit:
        if(not hi):
            hi = questionary.text("Say 'hi' to begin.").ask() == "hi"
        else:
            if(first_greet):
                print(f"hi {request_get('/users', api_key).json()['name']}. Hope you're having a lovely day!")
                first_greet = False
            action = questionary.select(
                        "What would you like to do?",
                        choices=["Log a habit", "Add or change a habit",
                                "Marvel at your own brilliance", 
                                "Just hang around for a bit", 
                                "Be an awesome force of nature somewhere else"]).ask()
            if(action == "Log a habit"):
                print("Great! Well done you!")
                habits = habits_get(api_key)
                print(habits)
                habit_names = [habit["name"] for habit in habits]
                if(len(habit_names) == 0):
                    print("You don't have any habits. Add some!")
                habit_names.append("Go back")
                selected_habit = questionary.select("What habit do you want to log?", choices= habit_names).ask()
                if(selected_habit == "Go back"):
                    continue
                print([habit['id'] for habit in habits if habit['name'] == selected_habit])
                habit_id = [habit['id'] for habit in habits if habit['name'] == selected_habit][0]
                habit_entry(api_key, habit_id)
                print("Habit logged! Well done you!")
            elif(action == "Add or change a habit"):
                choice = questionary.select("Righto. What would you like to do?",["Create a habit", "Change a habit", "Delete a habit", "View all habits", "Go back"]).ask()
                if(choice == "Create a habit"):
                    name = questionary.text("What is the name of the habit?").ask()
                    periodicity = questionary.text("How often do you want to log this habit?").ask()
                    completion_criteria = questionary.text("Tell me about how you want to complete this habit").ask()
                    habits_create(api_key, name, periodicity, completion_criteria)
                    print("Awesome! Habit created! Here's a list of your habits:")
                    habits = [habit["name"] for habit in habits_get(api_key)]
                elif(choice == "Change a habit"):
                    habits = habits_get(api_key)
                    habit_names = [habit["name"] for habit in habits]
                    if(len(habit_names) == 0):
                        print("You don't have any habits. Add some!")
                        continue
                    selected_habit = questionary.select("What habit do you want to change?", choices= habit_names).ask()
                    print([habit['id'] for habit in habits if habit['name'] == selected_habit])
                    habit_id = [habit['id'] for habit in habits if habit['name'] == selected_habit][0]
                    name = questionary.text("What is the name of the habit?").ask()
                    periodicity = questionary.text("How often do you want to log this habit?").ask()
                    completion_criteria = questionary.text("Tell me about how you want to complete this habit").ask()
                    habits_change(api_key, habit_id, name, periodicity, completion_criteria)
                    print("Habit changed! Here's a list of your habits:")
                    habits = [habit["name"] for habit in habits_get(api_key)]
                    print(habits)
                elif(choice == "Delete a habit"):
                    habits = habits_get(api_key)
                    habit_names = [habit["name"] for habit in habits]
                    if(len(habit_names) == 0):
                        print("You don't have any habits. Add some!")
                        continue
                    selected_habit = questionary.select("What habit do you want to delete?", choices= habit_names).ask()
                    print([habit['id'] for habit in habits if habit['name'] == selected_habit])
                    habit_id = [habit['id'] for habit in habits if habit['name'] == selected_habit][0]
                    confirm = questionary.confirm("Are you sure you want to delete this habit? This will delete all habit entries related to this habit. This is a destructive action.", default=False).ask()
                    if(confirm):
                        habit_delete(api_key, habit_id)
                        print("Habit deleted! Here's a list of your habits:")
                        habits = [habit["name"] for habit in habits_get(api_key)]
                        print(habits)
                    else: 
                        print("Thank goodness you didn't delete the habit. Here's a list of your habits:")
                        habits = [habit["name"] for habit in habits_get(api_key)]
                        print(habits)
                elif(choice == "View all habits"):
                    habits = [habit["name"] for habit in habits_get(api_key)]
                    print(habits)
                elif(choice == "Go back"):
                    continue
            elif(action == "Marvel at your own brilliance"):
                pass
            elif(action == "Just hang around for a bit"):
                questionary.text("Ok. Let's hang around for a bit. Pick a number... Any number...").ask()
                print("Awesome. I'm sure you picked a great number!")
            elif(action == "Be an awesome force of nature somewhere else"):
                exit = True
    print("Have a lovely day you magnificent human being!")
    

 


def api_key_flow() -> str:
    print("Locating Api Key...")
    global api_key
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