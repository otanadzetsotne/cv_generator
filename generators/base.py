import json
import os
import subprocess
from uuid import uuid4
from pathlib import Path
from tempfile import gettempdir
from generators.formatter import Formatter


class BaseGenerator:
    def __init__(self, templates_path):
        self.templates = templates_path

    def html(self, name):
        with open(os.path.join(self.templates, f'{name}.html'), 'r') as f:
            return Formatter(f.read())

    def header(self, cv):
        header = cv.get('header', {})
        info = cv.get('info', {})

        html = self.html('header')
        html = html.format(
            full_name=header.get('person', ''),
            vacancy=header.get('header', ''),
            address=info.get('address', ''),
            phone=info.get('phone', ''),
            email=info.get('email', ''),
            linked_in=info.get('linked_in', ''),
        )
        return html

    @staticmethod
    def base_content_body(content):
        if isinstance(content, list):
            ul = Formatter('<ul>$(li)</ul>')
            content = ''.join([f'<li>{c}</li>' for c in content])
            content = ul.format(li=content)

        return content

    @staticmethod
    def list_content_body(content):
        ul = Formatter('<ul>$(li)</ul>')
        content = ''.join([f'<li>{c}</li>' for c in content])
        return ul.format(li=content)

    def experience_content_body(self, contents):
        html = ''
        for content in contents:
            experience = self.html('experience')
            experience = experience.format(
                company=content.get('company', ''),
                position=content.get('position', ''),
                dates=content.get('dates', ''),
                experience=self.base_content_body(content.get('content', '')),
            )
            html += experience
        return html

    def contents(self, cv):
        html = Formatter('')
        contents = cv.get('content', [])

        for content in contents:
            body_generator = self.base_content_body
            subhead = content.get('subhead', '')

            content_body = content.get('content', '')
            if subhead == 'Professional Experience':
                body_generator = self.experience_content_body

            content_body_html = body_generator(content_body)
            html += self.html('content').format(subhead=subhead, content=content_body_html)

        return html

    def full(self, cv):
        # Get htmls
        full = self.html('main')
        header = self.header(cv)
        contents = self.contents(cv)

        # Create full html
        full = full.format(header=header, contents=contents)
        return full

    def generate(self, cv_json):
        cv = json.loads(cv_json)
        html = self.full(cv)

        tmp_dir = Path(gettempdir())
        file_prefix = str(uuid4())
        html_path = tmp_dir / f'{file_prefix}.html'
        pdf_path = tmp_dir / f'{file_prefix}.pdf'

        with open(html_path, 'w') as f:
            f.write(html)

        subprocess.check_output(['wkhtmltopdf', f'file://{html_path}', pdf_path])
        with open(pdf_path, 'rb') as f:
            pdf = f.read()

        return pdf
