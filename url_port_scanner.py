import socket
import datetime
import subprocess
import pyfiglet
from urllib.parse import urlparse
import threading

def scan_port(target, port, open_ports, closed_ports, lock):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    result = sock.connect_ex((target, port))
    sock.close()
    with lock:
        if result == 0:
            open_ports.append(port)
        else:
            closed_ports.append(port)

def scan_ports(target, start_port=1, end_port=1024):
    open_ports = []
    closed_ports = []
    lock = threading.Lock()
    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port, open_ports, closed_ports, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return open_ports, closed_ports

def save_results(target, hostname, open_ports, closed_ports):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_results_{hostname}_{target}_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(f"Port scan results for {hostname} ({target}) at {timestamp}\n\n")
        f.write(f"{'Port':<10}{'Status':<10}\n")
        for port in open_ports:
            f.write(f"{port:<10}{'Open':<10}\n")
        for port in closed_ports:
            f.write(f"{port:<10}{'Closed':<10}\n")
    print(f"Results saved to {filename}")

def ping_host(target):
    print(f"Pinging {target} to check connectivity...")
    try:
        output = subprocess.check_output(["ping", "-n", "4", target], universal_newlines=True)
        print(output)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to ping {target}. Host may be unreachable.")
        return False

def main():
    ascii_banner = pyfiglet.figlet_format("URL Port Scanner")
    print(ascii_banner)

    url_or_ip = input("Enter the URL or IP to scan (e.g. https://website.gov.pk/ or 8.8.8.8): ")

    # Add scheme if missing for proper parsing
    if not url_or_ip.startswith(('http://', 'https://')):
        url_or_ip = 'http://' + url_or_ip

    parsed_url = urlparse(url_or_ip)
    hostname = parsed_url.hostname

    # If input is a raw IP address, hostname will be None, so use input directly
    if hostname is None:
        hostname = url_or_ip

    try:
        ip = socket.gethostbyname(hostname)
        print(f"Resolved IP address of {hostname} is {ip}")
    except socket.gaierror:
        print(f"Failed to resolve IP for {hostname}")
        return

    if not ping_host(ip):
        print("Aborting port scan due to unreachable host.")
        return

    start_port = input("Enter start port (default 1): ")
    end_port = input("Enter end port (default 1024): ")

    start_port = int(start_port) if start_port.isdigit() else 1
    end_port = int(end_port) if end_port.isdigit() else 1024

    print(f"Scanning ports {start_port} to {end_port} on IP {ip}...")
    open_ports, closed_ports = scan_ports(ip, start_port, end_port)

    print(f"Open ports: {open_ports}")
    print(f"Closed ports: {closed_ports}")

    save_results(ip, hostname, open_ports, closed_ports)

if __name__ == "__main__":
    main()
