from cryptography.fernet import Fernet
import configparser

# Generiere einen Schlüssel und speichere ihn in einer Datei
key = Fernet.generate_key()
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

# Initialisiere Fernet mit dem Schlüssel
cipher_suite = Fernet(key)

# Anmeldedaten
username = "REST API ADMIN USERNAME"
api_key = "REST API ADMIN API KEY"

# Verschlüssele die Anmeldedaten
encrypted_username = cipher_suite.encrypt(username.encode()).decode()
encrypted_api_key = cipher_suite.encrypt(api_key.encode()).decode()

# Speichere die verschlüsselten Anmeldedaten in der config.ini-Datei
config = configparser.ConfigParser()
config['fortigate'] = {
    'username': encrypted_username,
    'api_key': encrypted_api_key
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)

print("Anmeldedaten wurden verschlüsselt und in config.ini gespeichert.")