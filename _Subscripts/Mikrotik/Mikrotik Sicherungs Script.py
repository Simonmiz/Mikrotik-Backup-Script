from paramiko import *
import csv
import datetime
import os
import shutil

# Jahreszhal variable
datum = datetime.datetime.now().strftime("%m-%Y")
now = datetime.datetime.now()

ausgabe = r"T:\MikroTik\Backups_Mikrotik\Backups_Mikrotik" + '-' + datum # Speicherort

## Versucht einen Ordner zu erstellen
## Falls dies scheitert Error message

try:
    os.mkdir(ausgabe)
    os.chmod(ausgabe, 0o777)
except Exception as E1:
    print(now.strftime("%H:%M:%S") + ' Fehler beim erstellen des Ordners', E1)

Kundeninfospfad = os.getcwd # Datei zum Auslesen
KIpfad = os.path.join(Kundeninfospfad, "KI.csv")
KI = KIpfad

with open(KI, "r") as f:

    # Erstelle einen Reader-Objekt
    reader = csv.reader(f, delimiter=";")

    # Durchlaufe die ganze Liste
    for row in reader:

        # Speichere die Daten aus der aktuellen Zeile in Variablen
        ip = row[0]
        port = row[1]
        user = row[2]
        pw = row[3]
        name = row[4]
    
        customername = name

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

        Backup_MT_CMD = "export" # Config Writeout Befehl
        stdin, stdout, stderr = client.exec_command(Backup_MT_CMD)

        output = stdout.readlines()

        with open(customername +'-' + str(datum) +".rsc", "w") as out_file:
            for line in output:
                out_file.write(line)

        # Ermittle den Pfad zur Datei "out_file"
        out_file_path = os.path.abspath(out_file.name)

        # Verschiebe die Datei "out_file" in den Ordner "technik"
        try:
            shutil.move(out_file_path, ausgabe)
            now = datetime.datetime.now()
            print(now.strftime("%H:%M:%S") + ' Mikrotik ' + ip + ' gesichert. (' + name +')')
        except Exception as E3:
            print(now.strftime("%H:%M:%S") + ' Fehler beim Verschieben der Datei:', E3)
        client.close()
