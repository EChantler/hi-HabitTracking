
import os
import subprocess
import sys
from app.cli.utils.process_utils import ProcessManager
def run_api():
    # return subprocess.Popen(["python", "-m", "app.api.run"])
    with open("api.log", "w") as log_file:
        # Redirect both stdout and stderr to the log file
        env = os.environ.copy()
        env["ENVIRONMENT"] = "development"
        return subprocess.Popen(["python", "-m", "app.api.run"], stdout=log_file, stderr=log_file, env=env)


def run_cli():
    return subprocess.Popen(["python", "-m" "app.cli.run"])

if __name__ == "__main__":
    api = run_api()
    cli = run_cli()
    ProcessManager.set_api_process(api)
    ProcessManager.set_cli_process(cli)
    api.wait()
    cli.wait()




    

# import asyncio
# import threading

# import uvicorn
# from app.api.init import app

# from app.core.dtos.user import UserRequest
# from app.core.services.habits import HabitsService
# from app.core.dtos.habit import HabitResponse

# from app.core.data.db import Session, User

# from app.core.data.db import Base, db
# from app.core.services.users import UsersService
# Base.metadata.create_all(db)

# # Create a session object
# session = Session()
# async def init():
#     us = UsersService(session)
#     if(session.query(User).count() == 0):
#         await us.add_user(UserRequest(name="test", email="test@test.com", apiKey="testApiKey"))
# # # Create an instance of HabitsService with the session object
# if __name__ == "__main__":
#     import uvicorn
#     import asyncio

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(init())

#     uvicorn.run(app, host="0.0.0.0", port=8000)

# print(us.get_all())

# hs = HabitsService(session)
# hs.add_habit(1, HabitDto(name="test_habit", completion_criteria="test_habit_completion_criteria", periodicity=1))
# print(hs.get_all(1))

# def run_api():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(init())
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# def cli_app():
#     # Here you can add your CLI functionality
#     # For example:
#     import time
#     while True:
#         print("CLI app running. Type 'exit' to quit.")
#         command = input(">>> ")
#         if command == 'exit':
#             break
#         else:
#             print(f"You entered: {command}")
#             # Add more CLI functionality as needed
#         time.sleep(1)

# if __name__ == "__main__":
#     api_thread = threading.Thread(target=run_api)
#     cli_thread = threading.Thread(target=cli_app)

#     api_thread.start()
#     cli_thread.start()

#     api_thread.join()
#     cli_thread.join()