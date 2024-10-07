import json
import os.path
import re
import sys
import time
from datetime import datetime
from random import shuffle, randint, choice, sample

from rich import print
from rich.box import ROUNDED
from rich.table import Table

self_ip = "192.168.0.100"
userDir = os.path.expanduser("~")
devices = [
    "Android Mobile Phone",
    "Apple Mobile Phone",
    "GUN/Linux Server",
    "Debian Server",
    "Microsoft Desktop",
    "Windows Desktop",
    "Mac Desktop",
    "Unknown",
    "Kali Linux",
]

ports = {
    21: "ftp",
    22: "ssh",
    25: "smtp",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    445: "microsoft-ds?",  # 仅Windows
    1433: "sql",  # 仅服务器
}

common_ports = [21, 22, 25, 80, 110, 143, 443]


def check_data_dir():
    if not os.path.exists(f"{userDir}/.mo/HackSystem/data"):
        os.makedirs(f"{userDir}/.mo/HackSystem/data")


def random_ips(num: int, start=101, end=256):
    ips = [f"192.168.0.{i}" for i in range(start, end)]
    shuffle(ips)
    return sorted(ips[:num])


def main():
    start_time = time.time()
    check_data_dir()
    show_router_info = True
    show_self_info = True

    code = sys.argv[1] if len(sys.argv) >= 2 else "--help"
    if code == "--help":
        print(
            "[green]使用方法: [red]nmap [blue]<IP Range>\n"
            "[green]例如: [red]nmap [blue]192.168.0.0-255\n"
            "[green]参数说明:\n"
            "    <IP Range>: 目标IP地址范围\n"
            "    --help: 显示帮助信息\n"
        )
        return
    if re.compile(r"192.168.0.\d+$").match(code):
        if not 0 <= int(re.compile(r"192.168.0.(\d+)").match(code)[1]) <= 255:
            print(
                "[red]错误的输入!\n"
                "具体信息: 输入的范围不在允许的范围内, ip地址应在0-255.0-255.0-255.0-255内"
            )
            return
        if int(re.compile(r"192.168.0.(\d+)").match(code)[1]) == 1:
            ips = []
            show_self_info = False
        elif 2 <= int(re.compile(r"192.168.0.(\d+)").match(code)[1]) <= 99:
            ips = []
            show_router_info = False
            show_self_info = False
        elif int(re.compile(r"192.168.0.(\d+)").match(code)[1]) == 100:
            ips = []
            show_router_info = False
        else:
            ips = [code] if choice([True, False]) else []
            show_router_info = False
            show_self_info = False
        ip_num = 1

    elif re.compile(r"192.168.0.\d+-\d+").match(code):
        start = int(re.compile(r"192.168.0.(\d+)-(\d+)").match(code)[1])
        end = int(re.compile(r"192.168.0.(\d+)-(\d+)").match(code)[2])
        if end <= start:
            print(
                "[red]错误的输入!\n"
                "具体信息: IP地址范围无意义"
            )
            return
        if not 0 <= start <= 255:
            print(
                "[red]错误的输入!\n"
                "具体信息: 输入的范围不在允许的范围内, ip地址应在0-255.0-255.0-255.0-255内"
            )
            return
        if not 0 <= end <= 255:
            print(
                "[red]错误的输入!\n"
                "具体信息: 输入的范围不在允许的范围内, ip地址应在0-255.0-255.0-255.0-255内"
            )
            return

        ip_num = end - start

        if end <= 99:
            ips = []
        else:
            if 0 not in range(start, end):
                show_router_info = False
            if 100 not in range(start, end):
                show_self_info = False
            start = start if start >= 101 else 101
            ips = random_ips(randint(1, end - start), start, end)

    else:
        print(
            "[red]错误的输入!\n"
            "[green]正确的输入参考: [red]nmap [blue]192.168.0.0-255\n"
            "[green]或者输入 [blue]--help [green]查看帮助"
        )
        return

    print("Starting Nmap 6.66(HSG) ( https://nmap.org ) at " + datetime.now().strftime("%Y-%m-%d %H:%M 中国标准时间"))
    data = {}
    if show_router_info:
        time.sleep(3)
        print(
            "Nmap scan report for 192.168.0.1 (192.168.0.1)\n"
            f"Host is up ({randint(10, 100) / 1000}s latency).\n"
            "Not shown: 999 filtered tcp ports (no-response)"
        )
        table = Table(box=ROUNDED)
        table.add_column("PORT")
        table.add_column("STATE")
        table.add_column("SERVICE")
        table.add_column("VERSION")
        table.add_row("80/tcp", "open", "http")
        print(table)
        print("")

    if show_self_info:
        time.sleep(3)
        print(
            f"Nmap scan report for {self_ip} ({self_ip})\n"
            f"Host is up ({randint(10, 100) / 1000}s latency).\n"
            "Not shown: 998 closed tcp ports (reset)"
        )
        table = Table(box=ROUNDED)
        table.add_column("PORT")
        table.add_column("STATE")
        table.add_column("SERVICE")
        table.add_column("VERSION")
        table.add_row("25/tcp", "filtered", "smtp")
        table.add_row("110/tcp", "filtered", "pop3")
        print(table)
        print("Service Info: OS: HSG(Debian) GUN/Linux; CPE: cpe:/o:mo:hsg")
        print("")

    for ip in ips:
        time.sleep(3)
        device = choice(devices)
        mac = ':'.join(
            [
                '%02X' % byte
                for byte in [randint(0x00, 0xfe) & 0xfe] + [randint(0x00, 0xff) for _ in range(6)]
            ]
        )
        port_num = 0 if device in ["Android Mobile Phone", "Apple Mobile Phone"] else randint(0, len(common_ports))
        port = sample(common_ports, port_num)
        if device in ["GUN/Linux Server", "Debian Server"]:
            port.append(1433)
            port_num += 1

        if device in ["Microsoft Desktop", "Windows Desktop"]:
            port.append(445)
            port_num += 1
        port.sort()

        print(
            f"Nmap scan report for {ip}\n"
            f"Host is up ({randint(10, 100) / 1000}s latency)."
        )
        if port_num == 0:
            print(f"All 1000 scanned ports on {ip} ({ip}) are in ignored states.")
        print(f"Not shown: {1000 - port_num} closed tcp ports (reset)")
        if port_num > 0:
            table = Table(box=ROUNDED)
            table.add_column("PORT")
            table.add_column("STATE")
            table.add_column("SERVICE")
            table.add_column("VERSION")
            for p in port:
                table.add_row(f"{p}/tcp", "open", ports[p])
            print(table)
        print(f"MAC Address: {mac} ({device})")
        print("")
        data.update(
            {
                ip: {
                    "device": device,
                    "mac": mac,
                    "open-ports": port
                }
            }
        )

    searched_num = len(ips)
    if show_router_info:
        searched_num += 1
    if show_self_info:
        searched_num += 1

    end_time = time.time()

    print(
        "Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .\n"
        f"Nmap done: {ip_num} IP addresses ({searched_num} hosts up) scanned in {end_time - start_time:.2f} seconds"
    )
    with open(f"{userDir}/.mo/HackSystem/data/devices.game", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()
