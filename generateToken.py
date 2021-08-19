import argparse
from yandex_music.client import Client

parser = argparse.ArgumentParser(description='Generate token file for other scripts')

parser.add_argument('-l', '--login', action="store", dest="login", required=True, help="Your Yandex login. Example: my-login@yandex.ru")
parser.add_argument('-p', '--password', action="store", dest="password", required=True, help="Your Yandex password.")
args = parser.parse_args()

client = Client.from_credentials(args.login, args.password)

with open('.token', 'w+') as file:
  file.seek(0)
  file.write(client.token)
  file.truncate()
  file.close()
print('Done!')