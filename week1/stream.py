from numpy import delete
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

# from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator

import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')


def add_data(author, title, article, postdate):
    c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',
              (author, title, article, postdate))
    conn.commit()


def view_all_notes():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data


def view_all_titles():
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    return data


def get_blog_by_title(title):
    c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data


def get_blog_by_author(author):
    c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
    data = c.fetchall()
    return data


def delete_data(title):
    c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
    conn.commit()


def readingTime(mytext):
    total_words = len([token for token in mytext.split(" ")])
    estimatedTime = total_words / 200.0
    return estimatedTime


title_temp = """
<div style = "background-color:#464e57; padding:10px, margin:10px; border-radius:10px">
<h4 style="color:white; text-align:center;">{}</h4>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; width:50px; height:50px; border-radius:50%;">
<h6 style="color:white; text-align:center;">Author: {}</h6>
<br/>
<br/>
<p style="text-align:justify">{}</p
<br/>


</div>
"""


def main():
    st.title("Simple Blog")

    menu = ['Home', 'View Posts', 'Add Post', 'Search', 'Manage']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        result = view_all_notes()
        # st.write(result)
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_article = str(i[2])[0:30]
            b_post_date = i[3]

            st.markdown(title_temp.format(b_title, b_author, b_article, b_post_date), unsafe_allow_html=True)

    elif choice == "View Posts":
        st.subheader("View Articles")
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("View Posts", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.text("Reading Time: {}".format((readingTime(b_article))))
            st.markdown(title_temp.format(b_title, b_author, b_article, b_post_date), unsafe_allow_html=True)





    elif choice == "Add Post":
        st.subheader("Add Article")
        create_table()
        blog_author = st.text_input("Enter Author Name", max_chars=50)
        blog_title = st.text_input("Enter Post Title")
        blog_article = st.text_area("Post Article Here", height=200)
        blog_post_date = st.date_input("Date")

        if st.button("Add"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success("Post:{} saved".format(blog_title))


    elif choice == "Search":
        st.subheader("Search Articles")
        search_term = st.text_input('Enter Search Term')
        search_choice = st.radio("Field to Search by", ("title", "author"))

        if st.button("Search"):

            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "author":
                article_result = get_blog_by_author(search_term)

            for i in article_result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                st.text("Reading Time: {}".format((readingTime(b_article))))

                st.markdown(title_temp.format(b_title, b_author, b_article, b_post_date), unsafe_allow_html=True)



    elif choice == "Manage":
        st.subheader("Manage Articles")

        result = view_all_notes()
        clean_db = pd.DataFrame(result, columns=["Author", "Title", "Articles", "Post Date"])
        st.dataframe(clean_db)

        unique_all_titles = [i[0] for i in view_all_titles()]
        delete_blog_by_title = st.selectbox("Unique Title", unique_all_titles)

        if st.button("Delete"):
            delete_data(delete_blog_by_title)
            st.warning("Deleted: '{}".format(delete_blog_by_title))

        if st.checkbox("Metrics"):
            new_df = clean_db
            new_df['Length'] = new_df['Articles'].str.len()
            st.dataframe(new_df)

            st.subheader("Author Stats")
            new_df["Author"].value_counts().plot(kind='bar')
            st.pyplot()

            st.subheader("Author Stats")
            new_df["Author"].value_counts().plot.pie(autopct="%1.1f%%")
            st.pyplot()


if __name__ == '__main__':
    main()