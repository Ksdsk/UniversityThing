import subprocess
import sys

commands = {
    "build": {
        "alias": ["build", "b"],
        "description": "Builds the project."
    },
    "local": {
        "alias": ["local", "l"],
        "description": "Runs the project locally."
    },
    "build-local": {
        "alias": ["build-local", "bl"],
        "description": "Builds the project and runs the project locally."
    },
    "deploy": {
        "alias": ["deploy", "d"],
        "description": "Deploys the project."
    },
    "set-profile-name": {
        "alias": ["set-profile-name", "spn"],
        "description": "Sets the AWS profile name."
    },
    "cmds": {
        "alias": ["cmds", "c"],
        "description": "Prints the list of commands."
    },
    "quit": {
        "alias": ["quit", "q"],
        "description": "Quits the program."
    }
}

def print_menu():
    print("EZSAM Menu")
    print("Type in `cmds` for a list of all commands.")
    print("Type in `quit` to exit.")
    print("--------------------------------------")

def print_commands():
    for key in commands:
        print(f"{key}: \n\t{commands[key]['description']}")
        print(f"\tAliases: {[alias for alias in commands[key]['alias']]}")
        print("")

def local_test(profile_name):

    if profile_name is None:
        profile_name = input("Enter profile name: ")

    f = open(".env", "r")
    pairs = []

    for line in f:
        if line.startswith("#"):
            continue
        
        key = ''.join(e for e in line.split("=")[0].title() if e.isalnum())
        value = line.split("=")[1].strip()
        pairs.append(f"{key}={value}")

    environment_variable_string = " ".join(pairs)
    print(environment_variable_string)

    command = ["sam", "local", "start-api", "--profile", profile_name, "--parameter-overrides", environment_variable_string]
    subprocess.run(command, shell=True)

def deploy(profile_name):

    if profile_name is None:
        profile_name = input("Enter profile name: ")

    f = open(".env", "r")
    pairs = []

    for line in f:
        if line.startswith("#"):
            continue
        
        key = ''.join(e for e in line.split("=")[0].title() if e.isalnum())
        value = line.split("=")[1].strip()
        pairs.append(f"{key}={value}")

    environment_variable_string = " ".join(pairs)
    print(environment_variable_string)

    command = ["sam", "deploy", "--profile", profile_name, "--parameter-overrides", environment_variable_string]
    subprocess.run(command, shell=True)


def run():
    profile_name = None

    # Get profile name from cmd line
    if len(sys.argv) > 1:
        profile_name = sys.argv[1]

    print_menu()

    while True:
        cmd = input("Enter command: ")

        if cmd in commands["build"]["alias"]:
            subprocess.run(["sam", "build"], shell=True)

        elif cmd in commands["local"]["alias"]:
            local_test(profile_name)

        elif cmd in commands["build-local"]["alias"]:
            subprocess.run(["sam", "build"], shell=True)
            local_test(profile_name)

        elif cmd in commands["deploy"]["alias"]:
            deploy(profile_name)

        elif cmd in commands["set-profile-name"]["alias"]:
            profile_name = input("Enter profile name: ")

        elif cmd in commands["cmds"]["alias"]:
            print_commands()

        elif cmd in commands["quit"]["alias"]:
            break

        else:
            print("Invalid command")

run()