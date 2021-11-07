import getpass
from .repl import start


def main():
    username = getpass.getuser()
    print("Hello {}! This is the Monkey programming language!".format(username))
    start()


if __name__ == '__main__':
    main()
