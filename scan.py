import sys
import socket
from datetime import datetime as dt


def main():
    # check argument length
    if len(sys.argv) == 2:
        # translate ip address to IPv4 (if network DNS identifies it)
        target_ip_address = socket.gethostbyname(sys.argv[1])

    else:
        print("Incomplete number of arguments given to scanner")
        print("Syntax: python3 scan.py <ip>")

    # Display Scanner Banner
    print("-" * 50)
    print(f"Scanning target {target_ip_address}")
    print(f"Time started: {str(dt.now())}")
    print("-" * 50)

    # attempt connection
    try:
        for target_port in range(4998, 5006):
            socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # time out if no response in 1sec
            socket.setdefaulttimeout(1)
            connection_status = socket_connection.connect_ex(
                (target_ip_address, target_port)
            )

            if connection_status == 0:
                print(f"Port {target_port} is open on ip {target_ip_address}")

    except KeyboardInterrupt:
        print("\n Scan manually interrupted!")
        sys.exit()

    except socket.gaierror:
        print(f"Hostname {target_ip_address} could not be resolved!")
        sys.exit()

    except socket.error:
        print(f"Could not establish a connection to target ip {target_ip_address} !")
        sys.exit()


main()
