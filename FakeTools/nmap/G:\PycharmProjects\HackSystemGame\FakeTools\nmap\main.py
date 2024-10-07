import sys
import re
from rich import print
from random import shuffle

ip = "192.168.0.101"




def random_ips(num: int):
    ips = [f"192.168.0.{i}" for i in range(102, 256)]
    shuffle(ips)
    return ["192.168.0.1"] + ips[:num]


def main():
    code = sys.argv[1]
    if code == "--help":
        print(
            "[green]使用方法: nmap <IP Range>\n"
            "例如: nmap 192.168.0.0-255\n"
            "参数说明:\n"
            "    <IP Range>: 目标IP地址范围\n"
            "    --help: 显示帮助信息\n"
        )
        return
    if not (re.compile(r"192.168.0.\d+").match(code)):
        print(
            "[red]错误的输入!\n"
            "正确的输入参考: nmap 192.168.0.0-255"
            "或者输入 --help 查看帮助"
        )
        return


if __name__ == '__main__':
    # main()
    print(random_ips(5))
