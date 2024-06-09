import time
import questionary
from app.cli.utils.process_utils import ProcessManager


def cli_app():
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
    try:
        with open('token.txt', 'r') as file:
            content = file.read()
            return content      
    except FileNotFoundError:
        has_token = questionary.confirm("Token not found. Do you have a token?").ask()
        if(has_token):
            token = questionary.text("What is your token?").ask()
            # check if the token is valid by doing an api-call

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