# -*- coding: utf-8 -*-
from controller import Controller


def main():
    controller = Controller('127.0.0.1', 54321)
    controller.run()


if __name__ == '__main__':
    main()