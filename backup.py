import os
import socket
from datetime import date, datetime, timedelta
import requests
import json

DIR_BASE = '/ '
LOCAL_HOST = socket.gethostname()
CONTAINER_NAME = ' '
DB = ['', '']
DB_USER = ''
DB_USER_PASSWORD = ''

DATE = date.today().strftime("%Y_%m_%d_%H_%M")
os.chdir(DIR_BASE)
os.mkdir(f"{LOCAL_HOST}_{DATE}")
os.system(f"chmod -R 700 {LOCAL_HOST}_{DATE}")

TIME_FIND = datetime.now() - timedelta(days=4)

for nome_arquivo in os.listdir(DIR_BASE):
    caminho_arquivo = os.path.join(DIR_BASE, nome_arquivo)
    if os.path.isfile(caminho_arquivo):
        time_find = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
        difference = datetime.now() - time_find
        if difference.days > 4:
            os.remove(caminho_arquivo)
            print(f"Arquivo {nome_arquivo} removido.")

for i in DB:
    MYSQL_DATE = f"{LOCAL_HOST}_{i}_{DATE}.sql.gz"
    CMD_BKP = f"mysqldump -u {DB_USER} -p{DB_USER_PASSWORD} {i} | gzip > {MYSQL_DATE}"
    os.system(f"docker exec {CONTAINER_NAME} {CMD_BKP}")

if os.path.isdir(os.path.join(DIR_BASE, f"{LOCAL_HOST}_{DATE}")):
    webhook_url = ""
    data = {
        "status": "sucesso",
        "message": "backup realizado com sucesso",
        "created_at": DATE
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
else:
    telegram_url = ""
    data = {
        "chat_id": "",
        "text": "Backup falhou",
        "disable_notification": True
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(telegram_url, data=json.dumps(data), headers=headers)
