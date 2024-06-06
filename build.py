import os
import subprocess
import sys


def create_requirements():
    try:
        import pipreqs
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pipreqs==0.5.0"]
        )

    try:
        subprocess.run(["pipreqs"], check=True)
        print(f"requirements.txt 檔案已生成")
    except subprocess.CalledProcessError as e:
        print(f"運行 pipreqs 失敗: {e}")


def build_application():
    try:
        import pyinstaller
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyinstaller==6.7"]
        )

    command = {
        "base": "pyinstaller",
        "options": ["--onefile", "--windowed"],
        "add_data": [
            {"source": "page", "destination": "page"},
            {"source": "inc", "destination": "inc"},
            {"source": "test_images", "destination": "test_images"},
            {"source": "config.json", "destination": "."},
        ],
        "script": "main.py",
        "icon": "test_images/logo.png",
    }

    # 動態生成命令
    command_list = [
        command["base"],
        *command["options"],
        f'--icon={command["icon"]}',
    ]

    for data in command["add_data"]:
        command_list.append(f'--add-data={data["source"]};{data["destination"]}')

    command_list.append(command["script"])

    try:
        # 執行 PyInstaller 命令
        subprocess.run(command_list, check=True)
        print("\033[92m" + "Build successful!" + "\033[0m")  # GREEN
    except subprocess.CalledProcessError as e:
        print("\033[91m" + f"Build failed: {e}" + "\033[0m")  # RED


if __name__ == "__main__":
    create_requirements()
    build_application()
