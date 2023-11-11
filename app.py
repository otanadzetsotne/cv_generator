import json
from pathlib import Path

import streamlit as st

from generators.formatter import Formatter
from generators.base import BaseGenerator

st.set_page_config(page_title="CV Generator", layout="wide")

ROOT_DIR = Path(__file__).parent
HTML_TEMPLATES_DIR = ROOT_DIR / 'templates' / 'html' / 'base'


# Default data

def example_prompt():
    with open(ROOT_DIR / 'templates' / 'prompt.txt', 'r') as f:
        return f.read()


def example_info():
    with open(ROOT_DIR / 'templates' / 'examples' / 'info.txt', 'r') as f:
        return f.read()


def example_experience():
    with open(ROOT_DIR / 'templates' / 'examples' / 'experience.txt', 'r') as f:
        return f.read()


def render_prompt(prompt_template, experience, info, vacancy):
    prompt_template = Formatter(prompt_template).format(
        information=info,
        experience=experience,
        vacancy=vacancy,
    )
    return prompt_template


# @st.cache_resource
def get_generator() -> BaseGenerator:
    return BaseGenerator(HTML_TEMPLATES_DIR)


# Logic

col_experience, col_info, col_vacancy = st.columns([2, 1, 1])

# Experience
col_experience.markdown('#### Professional experience', unsafe_allow_html=True)

experience = st.session_state['experience'] = col_experience.text_area(
    'cant be empty',
    value=st.session_state.get('experience', example_experience()),
    height=250,
    key='text_area_experience',
    label_visibility='collapsed',
)

# Personal information
col_info.markdown('#### Personal information', unsafe_allow_html=True)

user_info = st.session_state['user_info'] = col_info.text_area(
    'cant be empty',
    value=st.session_state.get('user_info', example_info()),
    height=250,
    key='text_area_info',
    label_visibility='collapsed',
)

# Vacancy text
col_vacancy.markdown('#### Vacancy text', unsafe_allow_html=True)

vacancy_text = st.session_state['vacancy_text'] = col_vacancy.text_area(
    'cant be empty',
    value=st.session_state.get('vacancy_text', ''),
    height=250,
    key='text_area_vacancy',
    label_visibility='collapsed',
)

col_template, col_prompt, col_cv = st.columns(3)

# Prompt template
col_template.markdown('#### Prompt template for LLM', unsafe_allow_html=True)

prompt_template = st.session_state['prompt_template'] = col_template.text_area(
    'cant be empty',
    value=st.session_state.get('prompt_template', example_prompt()),
    height=300,
    key='text_area_prompt_template',
    label_visibility='collapsed',
)

# Rendered prompt
col_prompt.markdown('#### Prompt for LLM', unsafe_allow_html=True)

prompt = st.session_state.get('prompt', '')
if col_prompt.button('Render prompt', use_container_width=True):
    prompt = render_prompt(prompt_template, experience, user_info, vacancy_text)
prompt = st.session_state['prompt'] = col_prompt.text_area(
    'cant be empty',
    value=prompt,
    height=246,
    key='text_area_prompt',
    label_visibility='collapsed',
)

# CV Json
col_cv.markdown('#### CV JSON', unsafe_allow_html=True)

cv = st.session_state['cv'] = col_cv.text_area(
    'cant be empty',
    value=st.session_state.get('cv', ''),
    height=246,
    key='text_area_cv',
    label_visibility='collapsed',
)

try:
    json.loads(cv)
    valid_cv = True
except json.JSONDecodeError as e:
    col_cv.error(f'Invalid JSON in CV\n{e}')
    valid_cv = False

if valid_cv:
    pdf = get_generator().generate(cv)
    col_cv.download_button('Download CV in pdf', data=pdf, file_name='cv.pdf', use_container_width=True)
