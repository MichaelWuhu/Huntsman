import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_bot):
        self.restart_bot = restart_bot

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Detected change in: {event.src_path}, restarting bot...")
            self.restart_bot()

class BotManager:
    def __init__(self):
        self.process = None

    def start_bot(self):
        print("Starting bot...")
        self.process = subprocess.Popen(['python', 'main.py'], cwd='bot')  # Adjust path as necessary

    def stop_bot(self):
        if self.process:
            print("Stopping bot...")
            self.process.terminate()
            self.process.wait()

    def restart_bot(self):
        self.stop_bot()
        self.start_bot()

if __name__ == "__main__":
    # Initialize the bot manager
    bot_manager = BotManager()
    bot_manager.start_bot()

    # Create a watchdog observer
    event_handler = ChangeHandler(bot_manager.restart_bot)
    observer = Observer()

    # Watch the bot's directory (update the path as needed)
    bot_directory = os.path.join(os.getcwd(), "bot")
    observer.schedule(event_handler, path=bot_directory, recursive=True)
    observer.start()

    print(f"Watching for file changes in {bot_directory}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping file watcher...")
        observer.stop()

    observer.join()
    bot_manager.stop_bot()
