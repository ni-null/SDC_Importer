import os
import subprocess

def build_application():
    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--add-data", "page;page",
        "--add-data", "inc;inc",
        "--add-data", "test_images;test_images",
        "main.py"
    ]

    try:
        # 執行 PyInstaller 命令
        subprocess.run(command, check=True)
        print("\033[92m" + "Build successful!" + "\033[0m")  # GREEN
    except subprocess.CalledProcessError as e:
        print("\033[91m" + f"Build failed: {e}" + "\033[0m")  # RED

if __name__ == "__main__":
    build_application()
