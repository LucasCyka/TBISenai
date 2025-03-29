from source.gui import GUI
from source.serial import SERIAL


def main():
    ser = SERIAL()
    gui = GUI(SERIAL)

    ser.run()
    gui.run()


if __name__ == '__main__':
    main()