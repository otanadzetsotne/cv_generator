from pathlib import Path

import streamlit as st

st.set_page_config(page_title="CV Generator", layout="wide")

ROOT_DIR = Path(__file__).parent


# Default data

def get_prompt():
    with open(ROOT_DIR / 'templates' / 'prompt.txt', 'r') as f:
        return f.read()


def get_info():
    with open(ROOT_DIR / 'templates' / 'examples' / 'info.txt', 'r') as f:
        return f.read()


def get_experience():
    with open(ROOT_DIR / 'templates' / 'examples' / 'experience.txt', 'r') as f:
        return f.read()


def render_prompt():
    return ''


# Logic

col_experience, col_info, col_vacancy = st.columns([2, 1, 1])

# Experience
col_experience.markdown('#### Professional experience', unsafe_allow_html=True)
experience = col_experience.text_area(
    '',
    value=get_experience(),
    height=250,
    key='text_area_experience',
    label_visibility='collapsed',
)

# Personal information
col_info.markdown('#### Personal information', unsafe_allow_html=True)
info = col_info.text_area(
    '',
    value=get_info(),
    height=250,
    key='text_area_info',
    label_visibility='collapsed',
)

# Vacancy text
col_vacancy.markdown('#### Vacancy text', unsafe_allow_html=True)
vacancy = col_vacancy.text_area(
    '',
    height=250,
    key='text_area_vacancy',
    label_visibility='collapsed',
)

col_template, col_prompt, col_cv = st.columns(3)

# Prompt template
col_template.markdown('#### Prompt template for GPT', unsafe_allow_html=True)
prompt_template = col_template.text_area(
    '',
    value=get_prompt(),
    height=300,
    key='text_area_prompt_template',
    label_visibility='collapsed',
)

# Rendered prompt
col_prompt.markdown('#### Prompt for GPT', unsafe_allow_html=True)
prompt = ''
if col_prompt.button('Render prompt', use_container_width=True):
    prompt = render_prompt()
prompt = col_prompt.text_area(
    '',
    value=prompt,
    height=250,
    key='text_area_prompt',
    label_visibility='collapsed',
)

# CV Json
col_cv.markdown('#### CV Json', unsafe_allow_html=True)
cv = col_cv.text_area(
    '',
    height=250,
    key='text_area_cv',
    label_visibility='collapsed',
)
col_cv.button('Generate CV pdf', use_container_width=True)
