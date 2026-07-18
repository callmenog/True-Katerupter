# Network analyzer/tester
import socket
import subprocess
import sys
import time

interface = "wlan0"
userinput = input


class Kate():
    def __init__(self):
        self.interface = interface
        self.userinput = userinput
        self.socker = socket
        self.time = time
        self.sys = sys
        self.subprocess = subprocess

    def start(self):
        print("Greetings br're lapin")
        if self.userinput == "exit" or self.userinput == "quit":
            self.sys.exit()
            print("Till again br're lapin")

    def scan(self, target, wlan0):
        if str(target).strip().lower() == "station scan":
            print("scanning...")
            commands = [
                ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
                ["iwlist", wlan0 or self.interface, "scan"],
            ]

            for command in commands:
                try:
                    result = self.subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                except FileNotFoundError:
                    continue

                if result.returncode == 0:
                    networks = self._parse_networks(result.stdout)
                    if networks:
                        for network in networks:
                            print(network)
                        return networks

            return []

        return None

    def _parse_networks(self, output):
        networks = []
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue

            if line.startswith("SSID:"):
                ssid = line.split("SSID:", 1)[1].strip()
            elif line.startswith("ESSID:"):
                ssid = line.split("ESSID:", 1)[1].strip().strip('"')
            elif line.startswith("Cell") and "Address" in line:
                continue
            else:
                ssid = None

            if ssid:
                networks.append(ssid)

        return networks

