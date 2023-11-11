import sys
from streamlit.web import cli as stcli
from pathlib import Path


if __name__ == '__main__':
    sys.argv = ["streamlit", "run", f"{Path(__file__).parent}/app.py"]
    sys.exit(stcli.main())
