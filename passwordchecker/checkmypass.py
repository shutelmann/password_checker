import requests
import hashlib
import sys


def get_api_response(first5_char):
    url = 'https://api.pwnedpasswords.com/range/' + first5_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f'Возможно ты накосячил с API, код ошибки: {response.status_code}, перепроверь API!'
        )
    return response


def check_pass_for_a_match(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def check_pass(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = get_api_response(first5_char)
    return check_pass_for_a_match(response, tail)


def main(args):
    print('Проверяем . . .')
    for password in args:
        count = check_pass(password)
        if count:
            if count == [2, 3, 4]:
                print(
                    f'Пароль: | {password} | был скомпрометирован {count} раза! Пора его менять, иначе тебя взломают!')
            else:
                print(
                    f'Пароль: | {password} | был скомпрометирован {count} раз! Пора его менять, иначе тебя взломают!')
        else:
            print(f'Поздравляю! Пароль: | {password} | не светился в инете!')
    return print('Проверка паролей звершена.')


if __name__ == '__main__':
    main(sys.argv[1:])
