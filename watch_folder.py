import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

upload_folder = os.getcwd() + '/' + os.getenv('UPLOAD_FOLDER')
    
def create_watch_folder():
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

class Watcher:
    FOLDER_TO_WATCH = upload_folder
    create_watch_folder()

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.FOLDER_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"[NEW FILE] {event.src_path}")
            subprocess.call(["python", "telegram_uploader.py"])

if __name__ == '__main__':
    w = Watcher()
    w.run()
