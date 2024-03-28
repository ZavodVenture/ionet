import argparse
from os import system
from time import sleep
import requests

def get_token():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14dGZka3BweHlmbG1tZ2x1bGxmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgwNDI1ODEsImV4cCI6MjAyMzYxODU4MX0.mNkDiJaCBB5twRNypzThEKl-s8d5VjasNyJj1l9BK9o'
    refresh_token = open('refresh_token').read().replace('\n', '')
    print(f'current token: {refresh_token}')

    try:
        r = requests.post('https://id.io.net/auth/v1/token?grant_type=refresh_token',
                          json={'refresh_token': refresh_token},
                          headers={'Apikey': token,
                                   'Authorization': f'Bearer {token}'})
    except Exception as e:
        raise Exception('Ошибка во время получения токена')
    else:
        r = r.json()

        if 'error' in r:
            raise Exception(r['error_description'])

        with open('refresh_token', 'w') as file:
            file.write(r['refresh_token'])
            file.close()

        return r['access_token']


def get_node_status(token):

    try:
        r = requests.get(f'https://production.io.systems/v1/io-worker/users/{args.user_id}/devices',
                         params={'page': 1,
                                 'page_size': 20},
                         headers={'Token': token})
    except Exception as e:
        raise Exception('Ошибка во время получения статуса ноды')
    else:
        r = r.json()

        if 'status' in r and r['status'] == 'succeed':
            return r['devices'][0]['status']
        else:
            raise Exception('Ошибка во время получения статуса ноды')


def reload():
    status = get_node_status(get_token())

    if status == 'down':
        system('sudo docker stop $(sudo docker ps -a -q); sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -a -q) -f')

        command = f'./launch_binary_linux --device_id={args.device_id} --user_id={args.user_id} --operating_system="Linux" --usegpus=false --device_name={args.device_name}'
        system(command)
        system(command)
    else:
        print(f'restart not needed: {status}')


def worker():
    while 1:
        sleep(int(args.delay))

        try:
            reload()
        except Exception as e:
            print(f'Ошибка: {e}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('device_id')
    parser.add_argument('user_id')
    parser.add_argument('device_name')
    parser.add_argument('delay')
    args = parser.parse_args()
    worker()
