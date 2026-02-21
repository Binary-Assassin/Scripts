import os
import argparse
import ipaddress

def sanitize_filename(name):
    """
    Expected format: IP_port_recurrance
    Example: 192.168.1.10_80_5
    """
    parts = name.split("_")

    if len(parts) < 2:
        return None

    ip_str = parts[0]
    port_str = parts[1]

    try:
        ip = ipaddress.IPv4Address(ip_str)
        port = int(port_str)

        if 0 < port <= 65535:
            return (int(ip), port)
    except:
        return None

    return None


def process_directory(directory, sort_flag=False):
    results = []

    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)

        if os.path.isfile(full_path):
            name_without_ext = os.path.splitext(filename)[0]
            sanitized = sanitize_filename(name_without_ext)

            if sanitized:
                results.append(sanitized)

    # Remove redundant entries
    results = list(set(results))

    # Sort if requested
    if sort_flag:
        results = sorted(results)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract IP:PORT from filenames in a directory.")
    parser.add_argument("-f", "--folder", required=True, help="Target directory path")
    parser.add_argument("-s", "--sort", action="store_true", help="Sort output in ascending order")
    parser.add_argument("-o", "--output", help="Optional output file")

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print("Invalid directory.")
        exit()

    data = process_directory(args.folder, args.sort)

    formatted_output = [
        f"{ipaddress.IPv4Address(ip)}:{port}"
        for ip, port in data
    ]

    if args.output:
        with open(args.output, "w") as f:
            for line in formatted_output:
                f.write(line + "\n")
    else:
        for line in formatted_output:
            print(line)
