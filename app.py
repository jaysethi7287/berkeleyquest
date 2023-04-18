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
DATA_URL = "vectorizedDB.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL
    df['embeddings'] = df['embeddings'].apply(ast.literal_eval)
    df = df.drop_duplicates(subset=['Class Description'], keep='first')
    return df

@st.cache_data
def semantic_search(search_query, df):
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
    dept = f"Dept: <a href='{result['Department URL']}'>{result['Department']}</a>" if pd.notnull(result['Department URL']) else result['Department']
    instruction_mode = f"{result['Instruction Mode']}"
    location = f"Location: <a href='{result['Building URL']}'>{result['Location']}</a>" if pd.notnull(result['Building URL']) else ""

    if isinstance(result['Location'], float):
        location = ""

    card_content = f"""
    <div class="card">
        <h3>{class_name}</h3>
        <p>{result['Units']} unit{'s' if result['Units'] != "1" else ''}  |  {result['Time']}  |  {result['Meets Days']} | {class_code}</p>
        <p>{result['Class Description']}</p>
        <p style='font-size: 14px; color: #ccc;'>{class_id} | {instruction_mode} | {dept} | {location}</p>
    </div>
    """

    st.markdown(card_style, unsafe_allow_html=True)
    st.markdown(card_content, unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='text-align: center;'>Berkeley Quest 🚀</h1>", unsafe_allow_html=True)

    search_query = st.text_input("✨  Search for a course:")

    if search_query:
        df = load_data()
        results = semantic_search(search_query, df)

        num_results = 7 # change the number of results to 7
        num_shown = 0

        while num_shown < num_results and num_shown < len(results):
            display_result_card(results.iloc[num_shown])
            num_shown += 1

    st.markdown("<div style='text-align: center; margin-top: 20px;'><a href='mailto:jayaditya@berkeley.edu?subject=Feedback%20-%20Berkeley%20Quest'>Leave feedback</a></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: 50px;'>Made with ♥︎ by Jayaditya Sethi</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 10px;'><a href='https://www.buymeacoffee.com/jaysethi' target='_blank'><img src='https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png' alt='Buy Me A Coffee' width='150' ></a></div>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()



# import ast
# import numpy as np
# import pandas as pd
# import streamlit as st
# import openai
# import os
# from openai.embeddings_utils import get_embedding
# from dotenv import load_dotenv
# #from google.cloud import storage
# import io
# from io import BytesIO

# # storage_client = storage.Client.from_service_account_json('/Users/jaysethi/Documents/Berkeley Course Scraper/googlestuff/berkeley-quest-92e8d66fb688.json')

# BUCKET_NAME = 'vectorizedclass'
# bucket = storage_client.get_bucket(BUCKET_NAME)
# blop = bucket.get_blob('vectorizedDB.csv')


# load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY")
# DATA_URL = "vectorizedDB.csv"

# @st.cache_data
# def load_data():
#     data = blop.download_as_string()
#     df = pd.read_csv(io.StringIO(data.decode('utf-8')))
#     df['embeddings'] = df['embeddings'].apply(ast.literal_eval)
#     df = df.drop_duplicates(subset=['Class Description'], keep='first')
#     return df


# @st.cache_data
# def semantic_search(search_query, df):
#     search_embedding = get_embedding(search_query, engine='text-embedding-ada-002')
#     embeddings = np.array(df["embeddings"].tolist())
#     similarities = np.dot(embeddings, search_embedding) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(search_embedding))
#     df["similarities"] = similarities
#     df.sort_values(by="similarities", ascending=False, inplace=True)
#     return df.head(15)

# def display_result_card(result):
#     card_style = """
#     <style>
#         .card {
#             background-color: #222222;
#             border: 1px solid #ccc;
#             border-radius: 4px;
#             box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
#             padding: 15px;
#             margin-bottom: 15px;
#         }
#     </style>
#     """

#     class_name = f"{result['Name']}"
#     class_code = f"Code: <a href='{result['Class URL']}'>{result['Class Code']}</a>"
#     class_id = f"Class ID: {result['Class ID']}"
#     dept = f"Dept: <a href='{result['Department URL']}'>{result['Department']}</a>" if pd.notnull(result['Department URL']) else result['Department']
#     instruction_mode = f"{result['Instruction Mode']}"
#     location = f"Location: <a href='{result['Building URL']}'>{result['Location']}</a>" if pd.notnull(result['Building URL']) else ""

#     if isinstance(result['Location'], float):
#         location = ""

#     card_content = f"""
#     <div class="card">
#         <h3>{class_name}</h3>
#         <p>{result['Units']} unit{'s' if result['Units'] != "1" else ''}  |  {result['Time']}  |  {result['Meets Days']} | {class_code}</p>
#         <p>{result['Class Description']}</p>
#         <p style='font-size: 14px; color: #ccc;'>{class_id} | {instruction_mode} | {dept} | {location}</p>
#     </div>
#     """

#     st.markdown(card_style, unsafe_allow_html=True)
#     st.markdown(card_content, unsafe_allow_html=True)

# def main():
#     st.markdown("<h1 style='text-align: center;'>Berkeley Quest 🚀</h1>", unsafe_allow_html=True)

#     search_query = st.text_input("✨  Search for a course:")

#     if search_query:
#         df = load_data()
#         results = semantic_search(search_query, df)

#         num_results = 7 # change the number of results to 7
#         num_shown = 0

#         while num_shown < num_results and num_shown < len(results):
#             display_result_card(results.iloc[num_shown])
#             num_shown += 1

#     st.markdown("<div style='text-align: center; margin-top: 20px;'><a href='mailto:jayaditya@berkeley.edu?subject=Feedback%20-%20Berkeley%20Quest'>Leave feedback</a></div>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; margin-top: 50px;'>Made with ♥︎ by Jayaditya Sethi</p>", unsafe_allow_html=True)
#     st.markdown("<div style='text-align: center; margin-top: 10px;'><a href='https://www.buymeacoffee.com/jaysethi' target='_blank'><img src='https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png' alt='Buy Me A Coffee' width='150' ></a></div>", unsafe_allow_html=True)



# if __name__ == "__main__":
#     main()