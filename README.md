# FortiGate Local-In Policy Generator

Dieses Repository enthält ein Python-Skript, das ein FortiGate CLI-Konfigurationsskript zur Generierung von "local-in policies" erstellt. Mithilfe der FortiGate REST API und eines Jinja2 Templates wird automatisch eine Konfiguration erzeugt, die es erlaubt, Management-Zugriffe über fest definierte IP-Ranges auf die WAN-Schnittstellen der FortiGate zu steuern.

---

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Funktionen](#funktionen)
- [Voraussetzungen](#voraussetzungen)
- [Installation und Setup](#installation-und-setup)
- [Verwendung](#verwendung)
- [Anpassung der Konfiguration](#anpassung-der-konfiguration)
- [Lizenz](#lizenz)

---

## Über das Projekt

Das **FortiGate Local-In Policy Generator**-Skript ist ein Hilfsmittel zur Automatisierung der Erstellung von Firewall-Konfigurationsskripten. Es kommuniziert mit der FortiGate über die REST API, um WAN-Schnittstellen und zugehörige IP-Adressen zu ermitteln, und generiert daraus ein CLI-Skript, welches:

- Adressobjekte für erlaubte IP-Ranges erstellt
- Adressgruppen zusammenstellt
- Benutzerdefinierte Service-Objekte konfiguriert
- Lokale In-Policies für die jeweiligen WAN-Interfaces anlegt

Dieses Tool ist besonders nützlich, um wiederkehrende Konfigurationsaufgaben zu vereinfachen und Fehler bei manuellen Eingaben zu vermeiden.

---

## Funktionen

- **Abfrage von WAN-Schnittstellen:** Das Skript ruft über die FortiGate REST API alle System-Interfaces ab und filtert dabei die WAN-Schnittstellen.
- **IP- und Maskenerkennung:** Es extrahiert die IP-Adresse und Subnetzmaske der gefundenen WAN-Interfaces.
- **Template-basierte Konfigurationsgenerierung:** Mit Jinja2 wird ein CLI-Skript erstellt, das:
  - Adressobjekte für definierte IP-Ranges generiert
  - Die WAN-IP-Konfiguration in Adressobjekte überführt
  - Eine Adressgruppe mit den erlaubten IPs zusammenstellt
  - Einen benutzerdefinierten Service für den Management-Port definiert
  - Zwei lokale In-Policies für jedes WAN-Interface erzeugt (einen für den erlaubten Zugriff und einen für den allgemeinen Zugriff)
- **Fehlerbehandlung:** Das Skript prüft, ob gültige WAN-Interfaces vorhanden sind und gibt entsprechende Fehlermeldungen aus.

---

## Voraussetzungen

- **Python 3**: Das Skript wurde mit Python 3 entwickelt.
- **Externe Bibliotheken**:
  - `requests` – für HTTP-Anfragen zur FortiGate API
  - `jinja2` – für die Template-Verarbeitung

Installiere die erforderlichen Pakete beispielsweise über `pip`:

```bash
pip install requests jinja2
```

---

## Installation und Setup

### Repository klonen

```bash
git clone https://github.com/dein-benutzername/fortigate_local-in_policy_generator.git
cd fortigate_local-in_policy_generator
```

### Konfigurationsanpassungen

Öffne das Skript `fortigate_local-in_policy_generator.py` und passe im Bereich der Konfiguration (oben im Skript) die Einträge in `ALLOWED_IPS` an. Trage hier die zulässigen IP-Ranges ein, z.B.:

```python
ALLOWED_IPS = [
    "197.268.12.15/30",
    "..."
]
```

Passe gegebenenfalls auch die Namen der Addressobjekte und Service-Objekte (`ALLOW_IP_GROUP`, `MGMT_SERVICE`) an.

---

## Verwendung

### Ausführen des Skripts

Starte das Skript über die Kommandozeile:

```bash
./fortigate_local-in_policy_generator.py
```

### Eingabeaufforderungen

- **FortiGate Host:** Gib die IP-Adresse oder den Hostnamen deiner FortiGate ein.
- **Management Port:** Gib den Management-Port deiner FortiGate ein.
- **REST API Key:** Gib deinen API-Schlüssel zur Authentifizierung ein.

### Ergebnis

Nach Eingabe der erforderlichen Daten generiert das Skript das FortiGate CLI-Konfigurationsskript, das anschließend im Terminal ausgegeben wird. Dieses Skript kann dann in der FortiGate CLI verwendet werden, um die lokale In-Policy entsprechend zu konfigurieren.

---

## Anpassung der Konfiguration

Falls du weitere Anpassungen vornehmen möchtest, kannst du das Jinja2 Template im Skript modifizieren. Das Template ist im Skript integriert und definiert die Struktur der generierten CLI-Befehle. Änderungen am Template ermöglichen es dir, zusätzliche Konfigurationsparameter oder alternative Strukturen zu implementieren.

---
