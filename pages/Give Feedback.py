from multiprocessing import connection
import streamlit as st
import base64
from PIL import Image
import sqlite3
st.set_page_config(page_title='Give Feedback', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)
def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])
    c1.markdown("##")
    c1.markdown(label)
    input_params.setdefault("key", label)
    return c2.text_input("", **input_params)
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
if __name__ == '__main__':
    add_bg_from_local('background.jpg')
    sqliteConnection = sqlite3.connect('feedbacks.db')
    cursor = sqliteConnection.cursor()
    #cursor.execute("DROP TABLE emp")
    sql_command = """CREATE TABLE IF NOT EXISTS emp (
    e_name VARCHAR(50),
    e_company VARCHAR(100),
    fb VARCHAR(2000),
    rate FLOAT);"""
    cursor.execute(sql_command)
    #st.image(img, width=400)
    original_title = '<p style="font-family:Georgia; color:#31704d; font-size: 60px;">FeedBack First</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    slogan = '<p style="font-family:Georgia; color:#834333; font-size: 38px;">We value your feedback</p>'
    st.markdown(slogan, unsafe_allow_html=True)
    # Form for collecting feedback
    with st.form("my_form", clear_on_submit=True):
        name = text_field("Name : ")
        company = text_field("Company Name :").lower()
        comment = st.text_area("Feedback :")
        rating = text_field("Rating :")
        if rating:
            rating = float(rating)

        #Storing details into database
        cursor.execute("insert into emp (e_name, e_company, fb, rate) values (?, ?, ?, ?)",
                    (name, company, comment, rating))
        sqliteConnection.commit()
        submit = st.form_submit_button(label="Submit")
    if submit:
        st.write('Your feedback was submitted successfully')
    cursor.close()
