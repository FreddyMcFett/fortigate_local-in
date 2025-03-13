# FortiGate Local-In Policy Script Generator

Das ist ein Python Script um automatisch per REST API ein Local-In Script zu generieren, dass nur erlaubte IPs auf das WAN Web-Interface zulässt.
Script meldet sich über einen REST API Admin han und holt schaut was für WAN Interfaces hat und welche eine IP-Adresse konfiguriert haben. Falls ein WAN Interface eine IP-Adresse konfiguriert hat, wird ein Script generiert um für das konfigurierte WAN Interface eine Local-In Policy zu erstellen.

Wichtig ist das erst mit dem encrypt_config.py ein verschlüsseltes Config File generiert wird, in der der REST API Admin Usernamer und Passwort steht.

Im ALLOWED_IPS Array kann man seine gewünschten IPs eintragen die whitelisted werden sollen.
