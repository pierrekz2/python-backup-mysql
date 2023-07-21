import requests
import os
import gzip
import shutil
import subprocess

DIR_BASE = '/'

DB = ('',)

DB_USER = ''

DB_USER_PASSWORD = ''

CONTAINER_NAME = ''

db_files = {
    '': '',
}

def send_telegram_message(message):
    bot_token = ""
    chat_id = ""

    data = {
        "chat_id": chat_id,
        "text": message,
        "disable_notification": True
    }

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.post(url, json=data)

for db_name in DB:
    print(f"Restaurando banco de dados: {db_name}")

    drop_query = f"DROP DATABASE IF EXISTS {db_name}"
    subprocess.run(["docker", "exec", CONTAINER_NAME, "mysql", "-u", DB_USER, "-p" + DB_USER_PASSWORD, "-e", drop_query])

    create_query = f"CREATE DATABASE {db_name}"
    subprocess.run(["docker", "exec", CONTAINER_NAME, "mysql", "-u", DB_USER, "-p" + DB_USER_PASSWORD, "-e", create_query])

    DIR = [os.path.join(DIR_BASE, name) for name in os.listdir(DIR_BASE) if os.path.isdir(os.path.join(DIR_BASE, name))]
    LAST_DIR = max(DIR, key=os.path.getctime)

    print(f"Último diretório criado encontrado: {LAST_DIR}")

    os.chdir(LAST_DIR)

    if db_name in db_files:
        sql_file = db_files[db_name]

        PATH_SQL = os.path.join(LAST_DIR, sql_file)

        if sql_file.endswith('.gz') and os.path.exists(PATH_SQL):
            try:
                with gzip.GzipFile(PATH_SQL, 'rb') as f_in:
                    f_in.peek(1)
            except (OSError, gzip.BadGzipFile):
                continue

            FILE_SQL = sql_file[:-3]
            PATH_DESTINY = os.path.join(LAST_DIR, FILE_SQL)

            print(f"Restaurando arquivo: {sql_file}")

            with gzip.open(PATH_SQL, 'rb') as f_in, open(PATH_DESTINY, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

            restore_cmd = f"docker exec -i {CONTAINER_NAME} mysql -u {DB_USER} -p{DB_USER_PASSWORD} {db_name} < {PATH_DESTINY}"

            try:
                subprocess.run(restore_cmd, shell=True, check=True)
                print(f"Restauração do banco de dados '{db_name}' concluída com sucesso.")
            except subprocess.CalledProcessError as e:
                print(f"Erro durante a restauração do banco de dados '{db_name}':")
                print(e.stderr.decode())
                send_telegram_message(f"Erro durante a restauração do banco de dados '{db_name}' no servidor '{CONTAINER_NAME}'. Detalhes do erro:\n{e.stderr.decode()}")

print("Processo concluído.")


def check_data_integrity():
    for db_name in DB:
        cmd_check = f"docker exec {CONTAINER_NAME} mysqlcheck -u {DB_USER} -p{DB_USER_PASSWORD} {db_name}"

        result_check = subprocess.run(cmd_check, shell=True, capture_output=True, text=True)

        if result_check.returncode == 0:
            print(f"A verificação de integridade para o banco de dados '{db_name}' foi concluída com sucesso.")
            print("Saída do mysqlcheck:")
            print(result_check.stdout)
        else:
            print(f"Ocorreu um erro durante a verificação de integridade para o banco de dados '{db_name}'.")
            print("Saída do mysqlcheck:")
            print(result_check.stderr)
            print("Executando REPAIR...")

            cmd_repair = f"docker exec {CONTAINER_NAME} mysqlcheck -u {DB_USER} -p{DB_USER_PASSWORD} --auto-repair --check {db_name}"
            result_repair = subprocess.run(cmd_repair, shell=True, capture_output=True, text=True)

            if result_repair.returncode == 0:
                print(f"O reparo do banco de dados '{db_name}' foi concluído com sucesso.")
            else:
                print(f"Ocorreu um erro durante o reparo do banco de dados '{db_name}'.")
                print("Saída do mysqlcheck - REPAIR:")
                print(result_repair.stderr)

check_data_integrity()