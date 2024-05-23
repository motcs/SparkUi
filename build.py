import subprocess

apps = [
    {"script": "SparkUi.py", "name": "妃妃Chat", "icon": "ffchat.ico"}
]

for app in apps:
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", app["name"],
        "--ico", app["icon"],
        app["script"]
    ])

# 直接命令行运行命令打包：
# pyinstaller --onefile --windowed --name=妃妃Chat --ico=ffchat.ico  --hidden-import=SparkApi.py SparkUi.py
