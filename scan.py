import argparse
import socket
import sys
from datetime import datetime as dt


def init():
    parser = argparse.ArgumentParser()

    parser.add_argument("-ip", "--target_ip_address", help="Target IP Address")
    parser.add_argument("-pr", "--port_range", help="Port Range to scan")
    parser.add_argument("-pc", "--port_common", help="Common Port Range")
    parser.add_argument("-v", "--verbose_level_1", help="Verbose Level 1", type=int)
    parser.add_argument("-vv", "--verbose_level_2", help="Verbose Level 2", type=int)
    parser.add_argument("-t", "--connection_timeout", help="Verbose Level 2", type=int)

    args = parser.parse_args()

    return args


def show_banner(messages):
    for message in messages:
        print(f"{message} \n")


def main():
    default_common_ports = [
        20,
        21,
        22,
        23,
        25,
        42,
        53,
        70,
        80,
        101,
        109,
        110,
        118,
        123,
        150,
        161,
        179,
        443,
        500,
        3000,
        3389,
        5000,
        8080,
    ]
    verbosity_level = 0

    connection_timeout = 1

    # set first 100 ports by default
    scan_port_range = [i + 1 for i in range(1000)]
    scan_args = init()
    scan_start_time = dt.now()

    # check argument has ip
    if scan_args.target_ip_address == None:
        print("No target ip address to scan")
        print(
            "syntax: scan.py [-h] [-ip TARGET_IP_ADDRESS] [-pr PORT_RANGE] [-pc PORT_COMMON] [-v VERBOSE_LEVEL_1] [-vv V]"
        )
        return

    else:
        # translate ip address to IPv4 (if network DNS identifies it)
        target_ip_address = socket.gethostbyname(scan_args.target_ip_address)

        if scan_args.connection_timeout is not None:
            connection_timeout = int(scan_args.connection_timeout)

        if scan_args.verbose_level_1 is not None:
            verbosity_level = 1

        if scan_args.verbose_level_2 is not None:
            verbosity_level == 2

        # get other args
        if scan_args.port_common is not None:
            scan_port_range = default_common_ports

        elif scan_args.port_range is not None and "-" in scan_args.port_range:
            scan_port_range = list(
                range(
                    int(scan_args.port_range.split("-")[0]),
                    int(scan_args.port_range.split("-")[1]),
                )
            )

        message_list = [
            "-" * 50,
            f"Scanning target {target_ip_address}",
        ]

        if verbosity_level >= 1:
            message_list.append(
                f"Time started: {str(dt.now())}",
            )

        message_list.append(
            "-" * 50,
        )

        # attempt connection
        show_banner(message_list)
        scan_start_time = dt.now()

        try:
            if verbosity_level == 2:
                print("Scanning initiated..")
            for target_port in scan_port_range:
                if verbosity_level == 2:
                    print(f"Scanning port {target_port} on {target_ip_address}")
                socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # time out if no response in 1sec
                socket.setdefaulttimeout(connection_timeout or 1)
                connection_status = socket_connection.connect_ex(
                    (target_ip_address, target_port)
                )

                if connection_status == 0:
                    print(f"Port {target_port} is open on ip {target_ip_address}")

                else:
                    if verbosity_level == 2:
                        print(f"Port {target_port} is not open")

            closing_message_list = [
                "-" * 50,
                f"Scanning target {target_ip_address} complete",
            ]

            if verbosity_level >= 1:
                closing_message_list.append(f"Time ended: {str(dt.now())}")

            if verbosity_level == 2:
                closing_message_list.append(
                    f"Scan ended in {str(scan_start_time - dt.now())}"
                )

            closing_message_list.append(
                "-" * 50,
            )

            show_banner(closing_message_list)

        except KeyboardInterrupt:
            print("\n Scan manually interrupted!")
            sys.exit()

        except socket.gaierror:
            print(f"Hostname {target_ip_address} could not be resolved!")
            sys.exit()

        except socket.error:
            print(
                f"Could not establish a connection to target ip {target_ip_address} !"
            )
            sys.exit()


main()
