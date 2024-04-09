from time import sleep
from paramiko import *
import csv
import datetime
import configparser
import shutil
import os

datum = datetime.datetime.now().strftime("%m-%Y")
now = datetime.datetime.now()

config = configparser.ConfigParser()
config.read('../../config/config.ini')
cg = config.get

ausgabe = cg("MIKROTIK", "save_location")
folder_name = cg("MIKROTIK", "folder_name")
list_name = cg("MIKROTIK", "list_name")
list_location = cg("GENERAL", "list_location")
delimiter = cg("GENERAL", "delimiter")

ausgabe = f"{ausgabe}/{folder_name}_{datum}"

list_csv = f"{list_csv}/{list_name}"

os.makedirs(ausgabe, exist_ok=True)
os.chmod(ausgabe, 0o777)

with open(list_csv, "r") as f:
    # Erstelle ein Reader-Objekt
    reader = csv.reader(f, delimiter=f"{delimiter}")

    # Durchlaufe die ganze Liste
    for row in reader:

        # Speichere die Daten aus der aktuellen Zeile in Variablen
        ip = row[0]
        port = row[1]
        user = row[2]
        pw = row[3]
        name = row[4]

        customer = name

        SSH_USER = user
        SSH_PASSWORD = pw
        SSH_HOST = ip
        SSH_PORT = int(port)
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S") + ' Verbindungsaufbau zu ' + SSH_HOST + ' wird hergestellt...')

        try:
            client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
        except Exception as E2:
            print(now.strftime("%H:%M:%S") + ' Fehler beim Verbindungsaufbau', E2)
            continue

        Backup_MT_CMD = "export"  # Config Print Befehl
        stdin, stdout, stderr = client.exec_command(Backup_MT_CMD)

        output = stdout.readlines()

        fn = customer + '-' + str(datum) + ".rsc"

        with open(fn, "w") as out_file:
            for line in output:
                out_file.write(line)

        shutil.move(fn, ausgabe)

        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S") + ' Mikrotik ' + ip + ' gesichert. (' + name + ')')
        client.close()
sleep(5)
