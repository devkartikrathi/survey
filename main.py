import streamlit as st
import os
import pandas as pd
import random
from PIL import Image

def save_to_csv(data, csv_filename):
    df = pd.DataFrame(data)
    df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)

def get_random_images(folder_path, num_images=1):
    images = os.listdir(folder_path)
    random_images = random.sample(images, min(num_images, len(images)))
    return [os.path.join(folder_path, img) for img in random_images]

def display_image_grid(images, columns=3):
    images = [img for sublist in images for img in sublist]
    for i in range(0, len(images), columns):
        cols = st.columns(columns)
        for j in range(columns):
            if i+j < len(images):
                cols[j].image(images[i+j], use_column_width=True)

def get_user_selection_images(batch_num, images):
    if f'batch_{batch_num}' not in st.session_state:
        st.session_state[f'batch_{batch_num}'] = []
    st.title(f'Batch {batch_num} - Choose 3 images:')
    st.session_state[f'batch_{batch_num}'] = st.multiselect('Select Images', images, st.session_state[f'batch_{batch_num}'], key=f'batch_{batch_num+30}')
    return st.session_state[f'batch_{batch_num}']

base_folder_images = 'img'
survey_csv_filename = 'survey_data.csv'

if 'text_answers' not in st.session_state:
    st.session_state['text_answers'] = ["", "", ""]
if 'selected_images' not in st.session_state:
    st.session_state['selected_images'] = [[], [], []]
if 'batch_images' not in st.session_state:
    st.session_state['batch_images'] = [[], [], []]

# Text-based Survey
if 'survey_page' not in st.session_state or st.session_state['survey_page'] == 'text':
    st.title('Text-based Survey')
    text_questions = [
        'What is your name?',
        'How satisfied are you with our service?',
        'Any suggestions or comments?'
    ]
    for i, question in enumerate(text_questions):
        st.session_state['text_answers'][i] = st.text_input(question, st.session_state['text_answers'][i])
    if st.button('Submit Text-based Survey'):
        st.session_state['survey_page'] = 'image1'
        st.experimental_rerun()

# Image-based Survey
for batch_num in range(3):
    if st.session_state.get('survey_page') == f'image{batch_num+1}':
        if not st.session_state['batch_images'][batch_num]:
            folders = os.listdir(base_folder_images)[batch_num*9:(batch_num+1)*9]
            st.session_state['batch_images'][batch_num] = [get_random_images(os.path.join(base_folder_images, folder)) for folder in folders]
        display_image_grid(st.session_state['batch_images'][batch_num])
        st.session_state['selected_images'][batch_num] = get_user_selection_images(batch_num+1, st.session_state['batch_images'][batch_num])
        if len(st.session_state['selected_images'][batch_num]) == 3:
            if batch_num < 2:
                st.session_state['survey_page'] = f'image{batch_num+2}'
            else:
                st.session_state['survey_page'] = 'submit'
            st.experimental_rerun()

# Save survey data to CSV on submit
if st.session_state.get('survey_page') == 'submit':
    survey_data = {
        'Name': [st.session_state['text_answers'][0]],
        'Satisfaction': [st.session_state['text_answers'][1]],
        'Comments': [st.session_state['text_answers'][2]],
        'Selected_Folders': [folder.split('/')[-1] for batch in st.session_state['selected_images'] for folder in batch]
    }
    save_to_csv(survey_data, survey_csv_filename)
    st.success('Survey submitted successfully!')
