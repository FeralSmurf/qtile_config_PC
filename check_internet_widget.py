import subprocess

def check_connectivity():
    try:
        subprocess.check_call(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.DEVNULL)
        return " 🌐 on "
    except subprocess.CalledProcessError:
        return " (╯°□°)╯ ┻━┻"

