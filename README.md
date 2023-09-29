# Mikrotik-backup-script

Gestartet am 27.9.2023

Eine CSV Datei wird benötigt die in der "KI" variable gelisted wird

CSV ist so aufgebaut

Spalte-1: SSH-Hostip
Spalte-2: SSH-Port
Spalte-3: SSH-Benutzername
Spalte-4: SSH-Passwort
Spalte-5: Konfigname

Die Variable technik ist der Speicherort + das ende ist der Ordner name und danach eine variable die Monat+Jahr als endung hinzufügt

Das Script verbindet sich via den Infos die in der KI CSV gelisted sind zu Mikrotiks und tut die konfig mit dem export befehl exportieren und dann in eine neue datei kopiert und abspeichert mit dem Konfignamen aus der CSV mit Monat+Jahr dahinter und dann .rsc als datei endung.
