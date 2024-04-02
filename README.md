# Backupscript - Mikrotik & Patton

Gestartet am 27.9.2023

Eine CSV Datei wird benötigt die in der "list_cv" variable gelisted wird

CSV ist so aufgebaut

Spalte-1: SSH-Hostip
Spalte-2: SSH-Port
Spalte-3: SSH-Benutzername
Spalte-4: SSH-Passwort
Spalte-5: Konfigname

Die Variable für list_csv wird in der config gespeichert

Das Script verbindet sich via den Infos die in der list_csv gelisted sind zu Mikrotiks/Pattons und tut die konfig mit dem export/show running-config befehl des Geräts exportieren,
und dann in eine neue datei kopiert und abgespeichert mit dem Konfignamen aus der CSV mit Monat+Jahr dahinter und dann .rsc für Mikrotik u. .cfg für Pattons als datei endung.
