import argparse
from os import system
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('device_id')
parser.add_argument('user_id')
parser.add_argument('device_name')
parser.add_argument('delay')
args = parser.parse_args()


def reload():
    command = f'./launch_binary_linux --device_id={args.device_id} --user_id={args.user_id} --operating_system="Linux" --usegpus=false --device_name={args.device_name}'
    system(command)
    sleep(2)
    system(command)


def worker():
    while 1:
        sleep(int(args.delay))
        reload()


if __name__ == '__main__':
    worker()
