import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class Utils:
    def __init__(self):
        pass

    async def ask_for_file(self):
        # Allowed file extensions
        file_extensions = [('Word Documents', '*.docx'),
                           ('Text Files', '*.txt')]

        # Create a root window but don't display it
        root = tk.Tk()
        root.withdraw()

        # Ask the user to select a file with the allowed extensions
        file_path = filedialog.askopenfilename(filetypes=file_extensions)

        # Check if a file was selected
        if not file_path:
            messagebox.showinfo("Info", "No file was selected.")
            return None
        else:
            return file_path

    async def clean_up_transcript(self, input_file):
        # Define a regex pattern for the timing lines to remove
        timing_pattern = re.compile(r"\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+")

        # Initialize an empty list to store the cleaned lines
        cleaned_lines = []

        # Read the contents of the file
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Process the lines
        for line in lines:
            # Remove the line if it matches the timing pattern
            if timing_pattern.match(line):
                continue
            # Check if line is not empty and not just a newline character
            elif line.strip():
                # Add the line in the format "Name (Country): [Comment]\n"
                cleaned_lines.append(f"{line.strip()}: ")
            # If the line is just a newline, we know the actual comment is next
            # So we read the next line to get the comment
            else:
                # Read next line for the comment
                comment = next(lines).strip()
                cleaned_lines.append(f"[{comment}]\n")

        # Join all the cleaned lines into a single string
        cleaned_transcript = ''.join(cleaned_lines)

        # Overwrite the input file with the cleaned transcript
        with open(input_file, 'w') as file:
            file.write(cleaned_transcript)

    async def file_to_oneliner(self, filepath):
        try:
            with open(filepath, 'r') as file:
                # Read the file contents
                contents = file.read()
                # Replace actual newlines with the literal \n string
                oneliner = contents.replace('\n', '\\n')
                # Wrap the oneliner in quotes
                oneliner_quoted = f'"{oneliner}"'
            return oneliner_quoted
        except FileNotFoundError:
            return "The file was not found."
        except Exception as e:
            return f"An error occurred: {e}"
