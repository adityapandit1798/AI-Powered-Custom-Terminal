import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import re
import readline  # For autocomplete
from colorama import Fore, Style, init

# Initialize colorama
init()

# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to query OpenAI's GPT model
def get_suggestion(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        suggestion = response.choices[0].message.content.strip()
        return suggestion
    except Exception as e:
        print(Fore.RED + f"Error querying AI: {e}" + Style.RESET_ALL)
        return "Unable to generate suggestion."

# Function to clean up text (remove ANSI escape codes and extra spaces)
def clean_text(text):
    # Remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    cleaned_text = ansi_escape.sub('', text).strip()
    return cleaned_text

# Autocomplete setup
def completer(text, state):
    try:
        # Get the current input line
        line = readline.get_line_buffer()
        words = line.split()
        if not words:  # Empty input
            return None

        # Get the last word being typed
        last_word = words[-1]

        # Check if the last word contains a path separator
        if "/" in last_word:
            base_dir, partial = os.path.split(last_word)
            base_dir = base_dir or "."  # Default to current directory if no base
        else:
            base_dir, partial = ".", last_word

        # List files and directories in the base directory
        try:
            options = os.listdir(base_dir)
        except FileNotFoundError:
            options = []

        # Filter options based on the partial match
        matches = [
            f"{base_dir}/{opt}/" if os.path.isdir(os.path.join(base_dir, opt)) else f"{base_dir}/{opt}"
            for opt in options if opt.startswith(partial)
        ]

        # Return the matching option based on the state
        if state < len(matches):
            return matches[state]
        else:
            return None
    except Exception as e:
        print(Fore.RED + f"Error in autocomplete: {e}" + Style.RESET_ALL)
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

# Main function to create the custom terminal
def custom_terminal():
    print(Fore.GREEN + "Welcome to the AI-Powered Custom Terminal!" + Style.RESET_ALL)
    print(Fore.YELLOW + "Type 'exit' to quit the terminal." + Style.RESET_ALL)
    print(Fore.CYAN + "Use 'ai <query>' to request AI assistance for a specific query." + Style.RESET_ALL)
    print(Fore.CYAN + "Example: ai which folder is this?" + Style.RESET_ALL + "\n")

    # Initialize the current working directory
    cwd = os.getcwd()

    # Load command history from file
    history_file = os.path.expanduser("~/.custom_terminal_history")
    try:
        with open(history_file, "r") as f:
            history = f.read().splitlines()
    except FileNotFoundError:
        history = []

    while True:
        try:
            # Update the prompt to show the current working directory
            prompt = Fore.CYAN + f"{cwd}$ " + Style.RESET_ALL

            # Prompt the user for input
            raw_command = input(prompt)

            # Handle empty commands
            if not raw_command.strip():
                continue

            # Exit the terminal if the user types 'exit'
            if raw_command.lower() == "exit":
                print(Fore.RED + "Exiting the AI-Powered Custom Terminal. Goodbye!" + Style.RESET_ALL)
                break

            # Add the command to history
            if raw_command.strip() != "history":
                history.append(raw_command.strip())

            # Handle the 'clear' command
            if raw_command.strip() == "clear":
                os.system('clear')  # Clear the screen
                continue

            # Handle the 'history' command
            if raw_command.strip() == "history":
                print(Fore.GREEN + "\n--- COMMAND HISTORY ---" + Style.RESET_ALL)
                for i, cmd in enumerate(history, start=1):
                    print(f"{i}. {cmd}")
                print(Fore.GREEN + "--- END HISTORY ---\n" + Style.RESET_ALL)
                continue

            # Check if the user wants AI assistance
            if raw_command.startswith("ai "):
                # Extract the query after 'ai '
                query = raw_command[3:].strip()
                if not query:
                    print(Fore.YELLOW + "Usage: ai <query> to request AI assistance." + Style.RESET_ALL)
                    continue

                # Generate an AI suggestion for the query
                prompt = f"Translate the following natural language query into a shell command: '{query}'"
                suggestion = get_suggestion(prompt)

                # Display the AI-generated command
                print(Fore.GREEN + "\n--- AI GENERATED COMMAND ---" + Style.RESET_ALL)
                print(suggestion)
                print(Fore.GREEN + "--- END GENERATED COMMAND ---\n" + Style.RESET_ALL)

                # Allow the user to modify the command
                modified_command = input(Fore.YELLOW + "Modify the command if needed (or press Enter to keep it): " + Style.RESET_ALL)
                final_command = modified_command.strip() if modified_command.strip() else suggestion

                # Confirm execution
                confirm = input(Fore.YELLOW + f"Do you want to execute this command? (y/n): " + Style.RESET_ALL).lower()
                if confirm == "y":
                    print(Fore.MAGENTA + f"Executing: {final_command}" + Style.RESET_ALL)
                    run_command(final_command, cwd)
                else:
                    print(Fore.YELLOW + "Command discarded." + Style.RESET_ALL)

            elif raw_command.startswith("cd "):
                # Handle directory changes
                target_dir = raw_command[3:].strip()
                try:
                    os.chdir(target_dir)  # Change the current working directory
                    cwd = os.getcwd()  # Update the current working directory
                except FileNotFoundError:
                    print(Fore.RED + f"Error: Directory '{target_dir}' not found." + Style.RESET_ALL)
                except NotADirectoryError:
                    print(Fore.RED + f"Error: '{target_dir}' is not a directory." + Style.RESET_ALL)

            else:
                # Highlight the executed command
                print(Fore.MAGENTA + f"Executing: {raw_command}" + Style.RESET_ALL)
                run_command(raw_command, cwd)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nUse 'exit' to quit the terminal." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)

    # Save command history to file
    with open(history_file, "w") as f:
        f.write("\n".join(history))

# Function to execute commands
def run_command(command, cwd):
    try:
        # Detect interactive commands
        if any(cmd in command for cmd in ["nano", "vim", "sudo", "ssh", "top", "htop", "less", "more"]):
            # Use os.system for interactive commands to preserve terminal behavior
            os.system(command)
        else:
            # Use subprocess.run for non-interactive commands
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
            output = result.stdout + result.stderr
            cleaned_output = clean_text(output)
            
            if result.returncode != 0:
                print(Fore.RED + f"Error: {cleaned_output}" + Style.RESET_ALL)
                
                # Ask the AI for a suggestion to fix the error
                prompt = f"The following command failed with this error: '{cleaned_output}'. Suggest a fix."
                suggestion = get_suggestion(prompt)
                
                # Display the AI-generated suggestion
                print(Fore.GREEN + "\n--- AI SUGGESTION TO FIX ERROR ---" + Style.RESET_ALL)
                print(suggestion)
                print(Fore.GREEN + "--- END SUGGESTION ---\n" + Style.RESET_ALL)
            else:
                print(cleaned_output)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nInterrupted by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    custom_terminal()
