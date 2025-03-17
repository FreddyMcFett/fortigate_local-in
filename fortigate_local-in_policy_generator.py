#!/usr/bin/env python3
import requests
import json
from jinja2 import Template





# ------------------------------
# Konfiguration – passe diese Werte nach Bedarf an
# ------------------------------
ALLOWED_IPS = [
    "IP-RANGE EINFUEGEN (z.B. 197.268.12.15/30)",
    "IP-RANGE EINFUEGEN",
    "IP-RANGE EINFUEGEN",
    "IP-RANGE EINFUEGEN"
]







ALLOW_IP_GROUP = "Allowed_IPs"  # Name des Addressobjekts
MGMT_SERVICE = "FGT_MGMT_Port"  # Name des Service-Objekts
# ------------------------------

# FortiGate Host, Management-Port und API-Key werden zur Laufzeit abgefragt
fortigate_host = input("FortiGate Host: ")
mgmt_port = input("Management Port: ")
api_key = input("REST API Key: ")

# SSL-Warnungen unterdrücken (bei selbst-signierten Zertifikaten)
requests.packages.urllib3.disable_warnings()

def get_wan_interfaces():
    """
    Ruft über die FortiGate-API die Interfaces ab und filtert die WAN-Interfaces.
    """
    url = f"https://{fortigate_host}:{mgmt_port}/api/v2/cmdb/system/interface"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except Exception as err:
        print("Fehler beim Abruf der Interface-Daten:", err)
        exit(1)
    data = response.json()
    return [iface for iface in data.get("results", []) if iface.get("role") == "wan"]

def get_wan_ip_and_mask(iface):
    """
    Ruft die WAN-IP und die Subnetzmaske des definierten Interfaces ab.
    """
    if 'ip' in iface and iface['ip']:
        ip_mask = iface.get("ip")
        ip, mask = ip_mask.split()
        return ip, mask
    else:
        print(f"Interface '{iface.get('name')}' hat keine IP-Adresse oder Subnetzmaske.")
        return None, None

# WAN-Interfaces abrufen
wan_interfaces = get_wan_interfaces()
if not wan_interfaces:
    print("Keine WAN-Interfaces gefunden.")
    exit(1)

# WAN-IPs und Subnetzmasken abrufen und in die Interfaces einfügen,
# dabei Interfaces mit der IP-Adresse 0.0.0.0 und Subnetzmaske 0.0.0.0 herausfiltern
valid_wan_interfaces = []
for iface in wan_interfaces:
    iface_ip, iface_mask = get_wan_ip_and_mask(iface)
    if iface_ip != "0.0.0.0" and iface_mask != "0.0.0.0":
        iface['ip'] = iface_ip
        iface['mask'] = iface_mask
        valid_wan_interfaces.append(iface)

# Jinja2 Template für das FortiGate CLI-Skript
template_str = """
config firewall address
    {% for ip in allowed_ips %}
    edit "Allowed_IP_{{ loop.index }}"
        set type ipmask
        set subnet "{{ ip }}"
    next
    {% endfor %}
    {% for iface in valid_wan_interfaces %}
    edit "{{ iface.name }}_IP"
        set type ipmask
        set subnet "{{ iface.ip }} {{ iface.mask }}"
    next
    {% endfor %}
end

config firewall addrgrp
    edit "{{ allow_ip_group }}"
        set member {% for ip in allowed_ips %}"Allowed_IP_{{ loop.index }}" {% if not loop.last %} {% endif %}{% endfor %}
    next
end

config firewall service custom
    edit "{{ mgmt_service }}"
        set tcp-portrange "{{ mgmt_port }}"
    next
end

config firewall local-in-policy
    {% for iface in valid_wan_interfaces %}
    edit {{ loop.index }}
        set intf "{{ iface.name }}"
        set srcaddr "{{ allow_ip_group }}"
        set dstaddr "{{ iface.name }}_IP"
        set action accept
        set service "{{ mgmt_service }}"
        set schedule "always"
    next
    edit {{ loop.index + valid_wan_interfaces|length }}
        set intf "{{ iface.name }}"
        set srcaddr "all"
        set dstaddr "{{ iface.name }}_IP"
        set service "{{ mgmt_service }}"
        set schedule "always"
    next
    {% endfor %}
end
"""

# Template rendern
template = Template(template_str)
config_script = template.render(
    allow_ip_group=ALLOW_IP_GROUP,
    allowed_ips=ALLOWED_IPS,
    valid_wan_interfaces=valid_wan_interfaces,  # Verwende die gefilterte Liste
    mgmt_service=MGMT_SERVICE,
    mgmt_port=mgmt_port
)

print("\nGeneriertes FortiGate CLI-Konfigurationsskript:\n")
print(config_script)