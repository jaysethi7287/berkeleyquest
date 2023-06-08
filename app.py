import ast
import numpy as np
import pandas as pd
import streamlit as st
import openai
import os
from openai.embeddings_utils import get_embedding
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
DATA_URL = "filt3.csv"

@st.cache_data
def blending_wonders():
    df = pd.read_csv(DATA_URL)
    df['embeddings'] = df['embeddings'].apply(ast.literal_eval)
    df['UnitDeranged'] = df['UnitDeranged'].apply(ast.literal_eval)
    return df

@st.cache_data
def brewing_magic(search_query, df):
    search_embedding = get_embedding(search_query, engine='text-embedding-ada-002')
    embeddings = np.array(df["embeddings"].tolist())
    similarities = np.dot(embeddings, search_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(search_embedding))
    df["similarities"] = similarities
    df.sort_values(by="similarities", ascending=False, inplace=True)
    return df.head(15)

def display_result_card(result):
    card_style = """
    <style>
        .card {
            background-color: #222222;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
            padding: 15px;
            margin-bottom: 15px;
        }
    </style>
    """

    class_name = f"{result['Name']}"
    class_code = f"Code: <a href='{result['Class URL']}'>{result['Class Code']}</a>"
    class_id = f"Class ID: {result['Class ID']}"
    dept_link = f"Dept: <a href='{result['Department URL']}'>{result['Department']}</a>" if pd.notnull(result['Department URL']) else result['Department']
    instruction_mode = f"{result['Instruction Mode']}"
    location = f"Location: <a href='{result['Building URL']}'>{result['Location']}</a>" if pd.notnull(result['Building URL']) else ""

    if isinstance(result['Location'], float):
        location = ""

    card_content = f"""
    <a href='{result['Class URL']}' style='text-decoration: none; color: inherit;'>
        <div class="card">
            <h3>{class_name}</h3>
            <p>{result['Units']} unit{'s' if result['Units'] != "1" else ''}  |  {result['Time']}  |  {result['Meets Days']} | {class_code}</p>
            <p>{result['Class Description']}</p>
            <p style='font-size: 14px; color: #ccc;'>{class_id} | {instruction_mode} | {dept_link} | {location}</p>
        </div>
    </a>
    """

    st.markdown(card_style, unsafe_allow_html=True)
    st.markdown(card_content, unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='text-align: center;'><a href='https://berkeley.streamlit.app/' style='text-decoration: none; color: inherit;'>BerkeleyQuest 🚀</a></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px; color: #ccc;'>Search your Fall 2023 courses using AI</p>", unsafe_allow_html=True)

    with st.expander('Add Filters'):
        st.write("More filters coming soon 👀")
        st.write('Units:')
        col1, col2, col3, col4, col5 = st.columns(5)
        unit_filters = {
            '1 Unit': False,
            '2 Units': False,
            '3 Units': False,
            '4 Units': False,
            '5+ Units': False,
        }
        unit_filters['1 Unit'] = col1.checkbox('1 Unit', value=unit_filters['1 Unit'])
        unit_filters['2 Units'] = col2.checkbox('2 Units', value=unit_filters['2 Units'])
        unit_filters['3 Units'] = col3.checkbox('3 Units', value=unit_filters['3 Units'])
        unit_filters['4 Units'] = col4.checkbox('4 Units', value=unit_filters['4 Units'])
        unit_filters['5 Units'] = col5.checkbox('5+ Units', value=unit_filters['5+ Units'])

        st.write("Course Level:")
        col1, col2, col3, col4 = st.columns(4)
        course_level_filters = {
            '99': False,
            '100': False,
            '200': False,
            '300': False,
        }

        course_level_filters['99'] = col1.checkbox('Lower Division', value=course_level_filters['99'])
        course_level_filters['100'] = col2.checkbox('Upper Division', value=course_level_filters['100'])
        course_level_filters['200'] = col3.checkbox('Graduate', value=course_level_filters['200'])
        course_level_filters['300'] = col4.checkbox('Professional', value=course_level_filters['300'])
        
    search_query = st.text_input("✨ Search for a course:", placeholder="Music but more techy...", key='search_input')
        
    if search_query:
        df = blending_wonders()
        
        # Filter by the selected units
        selected_unit_filters = [unit[0] for unit, value in unit_filters.items() if value]
        if selected_unit_filters:
            df = df[df['UnitDeranged'].apply(lambda x: any(val in selected_unit_filters for val in x))]
        
        # Filter by the selected course levels
        selected_level_filters = [unit[0] for unit, value in course_level_filters.items() if value]

        if selected_level_filters:
            df = df[df['DIV'].apply(lambda x: any(val in selected_level_filters for val in x))]

        results = brewing_magic(search_query, df)
        
        for i in range(10): # Always display the first 7 entries
            if i < len(results):
                display_result_card(results.iloc[i])
    st.markdown("<p style='text-align: center; margin-top: 10px; color: #ccc;'>🚨 If the text is illegible, set the theme to DARK: 3 lines on the top right > settings > theme: dark 🚨</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 5px;'><a href='mailto:jayaditya@berkeley.edu?subject=Feedback%20-%20Berkeley%20Quest'>Leave feedback</a></div>", unsafe_allow_html=True)
    #st.markdown("<p style='text-align: center; margin-top: 20px; color: #ccc;'>Currently in beta with upcoming features</p>", unsafe_allow_html=True)
    st.markdown("<hr margintop: 20px>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: 25;'>Made with ♥︎ by Jayaditya Sethi and Ethan Jagoda</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 10px;'><a href='https://www.buymeacoffee.com/jaysethi' target='_blank'><img src='https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png' alt='Buy Me A Coffee' width='150' ></a></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()