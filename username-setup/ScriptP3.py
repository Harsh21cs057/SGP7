import os
import subprocess
import shutil
import glob

# Get username from the environment variable
username = os.getenv("USERNAME")
if not username:
    print("USERNAME environment variable is not set. Please provide a username.")
    exit(1)

# Define output directories and filenames
output_dir = "./combined_output"
json_output_file = os.path.join(output_dir, f"{username}_combined_output.json")

# Ensure the combined output directory exists
os.makedirs(output_dir, exist_ok=True)

commands = [
    {
        "command": (
            f"bash -c 'cd maigret && source venv/bin/activate && "
            f"maigret {username} --json simple --folderoutput .{output_dir} && deactivate'"
        ),
        "output_file": f".{output_dir}/maigret_{username}.json"
    },
    {
        "command": f"cd sherlock && sherlock {username} --print-found --csv",
        "output_file": f"sherlock/{username}.csv",
        "move_to": os.path.join(output_dir, f"{username}.csv")
    },
    {
        "command": (
            f"bash -c 'cd socialscan && source venv/bin/activate && "
            f"socialscan {username} --json socialscan_{username}.json && deactivate'"
        ),
        "output_file": f"socialscan/socialscan_{username}.json",
        "move_to": os.path.join(output_dir, f"socialscan_{username}.json")
    },
    {
        "command": (
            f"bash -c 'cd blackbird && source venv/bin/activate && "
            f"python3 blackbird.py -u {username} --csv && deactivate'"
        ),
        "output_pattern": f"blackbird/results/{username}_*/{username}_*.csv",  # Pattern for blackbird output
        "move_to": os.path.join(output_dir, f"blackbird_{username}.csv")
    }
]

def run_command(command):
    """
    Run a shell command with UTF-8 encoding.
    """
    try:
        print(f"Running command: {command}")
        # Use subprocess to run the command
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Decode the output
            encoding="utf-8"  # Use utf-8 to handle special characters
        )
        print(f"Command output: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"Command stderr: {result.stderr.strip()}")
        print("Command completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Command stderr: {e.stderr.strip()}")
        if e.stdout:
            print(f"Command stdout: {e.stdout.strip()}")
    except UnicodeDecodeError as decode_error:
        print(f"Encoding error while running command: {decode_error}")

def move_file(source, destination):
    """
    Move a file from source to destination if it exists.
    """
    if os.path.exists(source):
        shutil.move(source, destination)
        print(f"Moved {source} to {destination}")
    else:
        print(f"Error: Expected output file {source} not found.")

# Run each command and move output files
for cmd in commands:
    run_command(cmd["command"])
    
    # Move output file to the combined folder if defined
    if "output_file" in cmd and "move_to" in cmd:
        move_file(cmd["output_file"], cmd["move_to"])

    # For Blackbird, use a glob pattern to find the actual CSV file
    elif "output_pattern" in cmd:
        matches = glob.glob(cmd["output_pattern"])
        if matches:
            for match in matches:
                move_file(match, cmd["move_to"])

print(f"All output files have been moved to {output_dir}")

