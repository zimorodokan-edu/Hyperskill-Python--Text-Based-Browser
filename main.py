import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init
import colorama
init(autoreset=True)

args = sys.argv
dir_ = args[1]


def ui():
    user_urls_cache = []
    history = []

    try:
        if not os.path.exists(dir_):
            os.mkdir(dir_)
    finally:
        pass

    while True:

        input_text = input().strip()

        if input_text not in ['back', 'exit']:
            if input_text.startswith('https://') or input_text.startswith('http://'):
                user_url = input_text
            else:
                user_url = 'https://' + input_text

            # file_path = dir_ + '/' + user_url.replace('https://', '').replace('http://', '')
            u_rev = user_url.replace(
                'https://', '').replace('http://', '')[::-1]
            short = (u_rev[u_rev.find('.') + 1:])[::-1]
            file_path = dir_ + '/' + short

            # print('user_url', user_url)
            # print('file_path', file_path)

            # if user_url not in user_urls_cache:
            if short not in user_urls_cache:
                try:
                    r = requests.get(user_url)
                    if 200 <= r.status_code < 400:
                        # with open(file_path, 'w', encoding='utf8') as f:
                        #     f.write(r.text)
                        text_to_save = []
                        # user_urls_cache.append(user_url)
                        user_urls_cache.append(short)
                        soup = BeautifulSoup(r.content, 'html.parser')
                        for tag in soup.find_all(['title', 'p', 'a', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul']):
                            if tag.string is not None:
                                if tag.name == 'a':
                                    # print(Fore.BLUE + tag.string)
                                    print(Fore.BLUE + tag.text)
                                else:
                                    # print(tag.string)
                                    print(tag.text)
                                text_to_save.append(tag.string)
                        with open(file_path, 'w', encoding='utf8') as f:
                            f.writelines('\n'.join(text_to_save))
                        # print(result)
                        # history.append(user_url)
                        history.append(short)
                    else:
                        print('Error: Incorrect URL')
                except Exception:
                    pass
                    print('Error: ConnectionError')

            else:
                with open(file_path, 'r', encoding='utf8') as f:
                    print(f.read())

                history.append(user_url)

            # print('user_url', user_url)
            # print('file_path', file_path)

        elif input_text == 'back':
            if len(history) > 1:
                history.pop()
                # user_url = history[len(history) - 1]
                # file_path = dir_ + '/' + user_url.replace('https://', '').replace('http://', '')
                short = history[len(history) - 1]
                file_path = dir_ + '/' + short
                with open(file_path, 'r', encoding='utf8') as f:
                    print(f.read())
            continue
        elif input_text == 'exit':
            break


ui()
