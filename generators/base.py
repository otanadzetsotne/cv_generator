import os
from generators.formatter import Formatter


class BaseGenerator:
    def __init__(self, templates_path, cv):
        self.cv = cv
        self.templates = templates_path

    def html(self, name):
        with open(os.path.join(self.templates, f'{name}.html'), 'r') as f:
            return Formatter(f.read())

    def header(self):
        cv = self.cv
        header = cv.get('header', {})
        info = cv.get('info', {})

        html = self.html('header')
        html = html.format(
            full_name=header.get('person'),
            vacancy=header.get('header'),
            address=info.get('address'),
            phone=info.get('phone'),
            email=info.get('email'),
            linked_in=info.get('linked_in'),
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

    def contents(self):
        html = Formatter('')
        contents = self.cv.get('content', [])

        for content in contents:
            body_generator = self.base_content_body
            subhead = content.get('subhead')

            content_body = content.get('content', '')
            if subhead == 'Professional Experience':
                body_generator = self.experience_content_body

            content_body_html = body_generator(content_body)
            html += self.html('content').format(subhead=subhead, content=content_body_html)

        return html

    def full(self):
        # Get htmls
        main = self.html('main')
        header = self.header()
        contents = self.contents()

        # Create full html
        main = main.format(header=header, contents=contents)
        return main
