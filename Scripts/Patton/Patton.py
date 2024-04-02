import csv
import datetime
import os
import shutil
import configparser
from time import sleep
from paramiko import *

datum = datetime.datetime.now().strftime("%m-%Y")
now = datetime.datetime.now()

config = configparser.ConfigParser()
config.read('../../config/config.ini')
cg = config.get

outputfile = cg("PATTON", "save_location")
folder_name = cg("PATTON", "folder_name")
list_csv = cg("GENERAL", "lists")
delimiter = cg("GENERAL", "delimiter")

outputfile = f"{outputfile}/{folder_name}_{datum}"

list_csv = f"{list_csv}/patton.csv"

try:
    os.mkdir(outputfile)
    os.chmod(outputfile, 0o777)
except Exception as E1:
    print(now.strftime("%H:%M:%S") + ' Fehler beim erstellen des Ordners', E1)

try:
    with open(list_csv, "r") as f:
        reader = csv.reader(f, delimiter=";")
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
            SSH_PORT = port
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())

            now = datetime.datetime.now()
            print(now.strftime("%H:%M:%S") + ' Verbindungsaufbau zu ' + SSH_HOST + ' wird hergestellt...')

            try:
                client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
            except Exception as E2:
                print(now.strftime("%H:%M:%S") + ' Fehler beim Verbindungsaufbau', E2)
                continue
            channel = client.invoke_shell()

            Backup_PT_CMD = "show running-config"  # Config Print Befehl
            channel.send(Backup_PT_CMD + "\n")

            sleep(10)

            data = channel.recv(20480)
            output = data

            output = output.decode("utf-8")

            fn = customer + '-' + str(datum) + ".cfg"

            with open(fn, "w") as out_file:
                for line in output:
                    out_file.write(line)

            # Ermittle den Pfad zur Datei "out_file"
            out_file_path = os.path.abspath(out_file.name)

            # Verschiebe die Datei "out_file" in den Ordner "technik"
            try:
                shutil.move(fn, outputfile)
                now = datetime.datetime.now()
                print(now.strftime("%H:%M:%S") + ' Patton ' + ip + ' gesichert. (' + name + ')')
            except Exception as E3:
                print(now.strftime("%H:%M:%S") + ' Fehler beim Verschieben der Datei:', E3)
            channel.close()
except Exception as E4:
    print(E4)
sleep(5)
