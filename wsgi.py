import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pobuilds import app as application


if __name__ == "__main__":
    application.run()
