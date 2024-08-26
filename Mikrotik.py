import configparser
import csv
import datetime
import os
import shutil
from time import sleep

from paramiko import SSHClient, AutoAddPolicy

# Heutiges Datum herausfinden für Dateibenennung
current_date = datetime.datetime.now().strftime("%m-%Y")
current_time = datetime.datetime.now()

# Config-Datei auslesen
config = configparser.ConfigParser()
config.read('config/config.ini')
get_config = config.get

# Konfigurationswerte aus der Datei abrufen
backup_directory = get_config("MIKROTIK", "outlocation")
backup_folder_name = get_config("MIKROTIK", "outfolder")
device_list_file = get_config("MIKROTIK", "list_file")
csv_delimiter = get_config("GENERAL", "delimiter")

# Pfad zum Ausgabeordner vorbereiten
backup_output_path = f"{backup_directory}/{backup_folder_name}_{current_date}"

# Ausgabeordner erstellen, falls er nicht existiert
os.makedirs(backup_output_path, exist_ok=True)

# Geräteliste aus CSV-Datei auslesen
with open(device_list_file, "r") as csv_file:
    reader = csv.reader(csv_file, delimiter=csv_delimiter)

    for row in reader:
        # Leere oder fehlerhafte Zeilen überspringen
        if len(row) < 5 or not row[0]:
            print("Überspringe leere oder fehlerhafte Zeile:", row)
            continue

        # Geräteinformationen aus der CSV-Zeile extrahieren
        device_ip = row[0]
        ssh_port = row[1]
        ssh_username = row[2]
        ssh_password = row[3]
        device_name = row[4]

        # IP-Adresse des Geräts und Login-Benutzername anzeigen
        print(current_time.strftime("%H:%M:%S") + f' Versuche Verbindung zu {device_ip} mit Benutzername "{ssh_username}"')

        # SSH-Client-Verbindung vorbereiten
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        current_time = datetime.datetime.now()
        print(current_time.strftime("%H:%M:%S") + ' Verbindung zu ' + device_ip + ' wird hergestellt...')

        try:
            # SSH-Port in Integer umwandeln und Verbindung herstellen
            ssh_port = int(ssh_port)
            ssh_client.connect(
                device_ip,
                port=ssh_port,
                username=ssh_username,
                password=ssh_password,
                allow_agent=False,         # SSH-Agent-Weiterleitung deaktivieren
                look_for_keys=False        # Suche nach SSH-Schlüsseln in ~/.ssh deaktivieren
            )
        except ValueError:
            print(current_time.strftime("%H:%M:%S") + f" Ungültiger Portwert: {ssh_port}. Zeile wird übersprungen.")
            continue
        except Exception as e:
            print(current_time.strftime("%H:%M:%S") + ' Verbindungsaufbau fehlgeschlagen:', e)
            continue

        # Backup-Befehl ausführen
        backup_command = "export"  # Befehl zum Exportieren der Konfiguration
        stdin, stdout, stderr = ssh_client.exec_command(backup_command)

        # Befehlausgabe lesen
        backup_output = stdout.readlines()

        # Dateinamen für die Sicherung erstellen
        backup_filename = f"{device_name}-{current_date}.rsc"

        try:
            # Befehlsausgabe in die Datei schreiben
            with open(backup_filename, "w") as backup_file:
                for line in backup_output:
                    backup_file.write(line)

            # Sicherungsdatei in den Ausgabeordner verschieben
            shutil.move(backup_filename, backup_output_path)

            current_time = datetime.datetime.now()
            print(current_time.strftime("%H:%M:%S") + f' Backup von {device_ip} ({device_name}) abgeschlossen.')
        except Exception as e:
            print(current_time.strftime("%H:%M:%S") + f' Fehler beim Schreiben oder Verschieben der Datei von {device_ip} ({device_name}):', e)

        # SSH-Verbindung schließen
        ssh_client.close()

# Verzögerung bevor das Skript beendet wird
sleep(5)
