from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
import os
import time
import datetime
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
target_channel = os.getenv('TELEGRAM_CHANNEL')
upload_folder = os.getcwd() + '/' + os.getenv('UPLOAD_FOLDER')

# ==== Configuration ====
log_file = 'upload_log.txt'
ignore_files = ['uploader_session', 'uploader_session.session', 'uploader_session.session-journal', 'telegram_uploader.py', log_file]
max_file_size = 2 * 1024 * 1024 * 1024  # 2GB

# ==== Load previously uploaded files ====
if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        uploaded_files = set(line.strip() for line in f.readlines())
else:
    uploaded_files = set()

# ==== Start Client ====
client = TelegramClient('uploader_session', api_id, api_hash)
client.start()

uploaded_this_session = []

def is_file_valid(file_path):
    filename = os.path.basename(file_path)
    return (
        os.path.isfile(file_path) and
        os.path.getsize(file_path) <= max_file_size and
        filename not in ignore_files and
        filename not in uploaded_files
    )

def log_upload(file_name):
    with open(log_file, 'a') as f:
        f.write(file_name + '\n')
    uploaded_this_session.append(file_name)
    
def create_watch_folder():
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
def get_day_of_week():
    weekday_num = datetime.datetime.today().weekday()
    match weekday_num:
        case 0:
            return 'Monday'
        case 1:
            return 'Tuesday'
        case 2:
            return 'Wednesday'
        case 3:
            return 'Thursday'
        case 4:
            return 'Friday'
        case 5:
            return 'Saturday'
        case 6:
            return 'Sunday'


create_watch_folder()

print("🚀 Starting upload...")

for root, _, files in os.walk(upload_folder):
    for file in tqdm(files, desc="Uploading files", unit="file"):
        file_path = os.path.join(root, file)
        dow = get_day_of_week()
        caption = 'Eufuria 2026: The Black Pawrade - ' + dow

        if not is_file_valid(file_path):
            continue

        try:
            print(f"[UPLOAD] Sending {file}")
            client.send_file(target_channel, file_path, caption=caption)
            log_upload(file)
            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] Failed to send {file}: {e}")
            time.sleep(30)


print("✅ Upload finished.")
client.disconnect()
