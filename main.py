"""
Entry script for the application
"""

import subprocess
import sys
import os

from kindgen import logger


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        subprocess.run(["streamlit", "run", "interface/main.py"], check=True)
    except subprocess.CalledProcessError as e:
        logger.critical(f"An error occurred while launching the application: {e}")
    except KeyboardInterrupt:
        logger.info("\nApplication interrupted. Exiting gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    main()
