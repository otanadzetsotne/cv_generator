import json
from pathlib import Path

from generators.base import BaseGenerator


root_dir = Path(__file__).parent
cv_path = root_dir / 'test.cv.json'
html_path = root_dir / 'templates' / 'html' / 'base'

with open(cv_path, 'r') as f:
    cv = json.load(f)


generator = BaseGenerator(templates_path=html_path, cv=cv)
html = generator.full()

with open(root_dir / 'test.html', 'w') as f:
    f.write(html)
