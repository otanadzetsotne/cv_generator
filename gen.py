import json
import subprocess
from pathlib import Path

from generators.base import BaseGenerator


root_dir = Path(__file__).parent
cv_path = root_dir / 'test.cv.json'
templates_path = root_dir / 'templates' / 'html' / 'base'

with open(cv_path, 'r') as f:
    cv = json.load(f)


generator = BaseGenerator(templates_path=templates_path, cv=cv)
html = generator.full()

html_path = root_dir / 'test.html'
with open(html_path, 'w') as f:
    f.write(html)

pdf_path = root_dir / 'test.pdf'
subprocess.check_output(['wkhtmltopdf', f'file://{html_path}', pdf_path])
