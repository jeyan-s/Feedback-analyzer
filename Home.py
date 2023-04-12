import streamlit as st
import base64
st.set_page_config(page_title='Give Feedback', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('world.jpg')
original_title = '<p style="font-family:Georgia; color: whitesmoke ; font-size: 45px;">Welcome to FR World</p>'
st.markdown(original_title, unsafe_allow_html=True)
with st.expander('', expanded=True):
    st.markdown(f'''
    <ul>
      <li><p style="font-size:25px; font-family:Georgia;">FR World holds Feedback and Reviews of organizations<p>
      </li>
      <li><p style="font-size:25px; font-family:Georgia;">Sharing information on what can be improved helps optimize</p> <p style="font-size:25px; font-family:Georgia;">the work process and get things done in less time</p></li>
      <li><p style="font-size:25px; font-family:Georgia;">Reviews provide insight into many areas, from culture</p><p style="font-size:25px; font-family:Georgia;"> of organization to competence in specific area</p></li>
    </ul>
    ''', unsafe_allow_html=True)
