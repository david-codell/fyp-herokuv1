import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Change the path in env based on your local path
MICROSERVICE_PATH = "C:\\xampp\\htdocs\\FYP-PYTHON\\AWS_FYP_PYTHON\\microservices\\"

def run_app(command):
    subprocess.Popen(command, shell=True)

if __name__ == '__main__':
    # Specify the commands to run each microservice
    commands = [
        f'python {MICROSERVICE_PATH}user.py', #port 8080
        f'python {MICROSERVICE_PATH}venue.py', #8081
        f'python {MICROSERVICE_PATH}category.py', #8082
        # f'python {MICROSERVICE_PATH}event.py', #8083
        f'python {MICROSERVICE_PATH}marketing.py', #8084
        f'python {MICROSERVICE_PATH}vendor.py', #8085
        f'python {MICROSERVICE_PATH}seatMap.py', #8086
        # Add more commands for other microservices as needed
    ]

    # Start each microservice in a separate subprocess
    for command in commands:
        run_app(command)