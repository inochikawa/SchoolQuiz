import os
import sys

# insert root directory into python module search path
rootPath = os.path.dirname(os.path.realpath(__file__ + "./../../../"))
sys.path.insert(0, rootPath)

from dotenv import load_dotenv

# load env variables
load_dotenv()

from frames import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
