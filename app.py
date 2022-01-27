from random import choice
from numpy import delete
import streamlit as st
import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

@st.cache()
def load_data(nrows):
    data = pd.read_csv("all_data.csv", nrows=nrows)
    return data

all_data = load_data(190000)


def main():
    st.title("Sales Analysis")

    menu = ['Home', 'Result of analysis']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'Home':
        st.subheader("Home")
        st.write(all_data)

        # months = range(1,13)
    

        # df = pd.DataFrame(all_data, columns = ['Sales', 'Month'])
        # st.bar_chart(all_data['Month'])
    
    elif choice == 'Result of analysis':
        st.subheader("Analysis")
        
        if st.checkbox('Best month'):
            # months = range(1,13)
    
            # st.write('Best month for sales')
            # df = pd.DataFrame(all_data, columns = ['Sales', 'Month'])
            # st.bar_chart(all_data['Month'])

            results = all_data.groupby('Month').sum()
            results = results/1000000
            months = range(1,13)
            plt.bar(months, results['Sales'])
            plt.xticks(months)
            plt.ylabel('Sales in USD')
            plt.xlabel('Month number')
            plt.show()
            st.pyplot()

        if st.checkbox('Best city'):
                
            st.write('Best city for sales')
            # df = pd.DataFrame(all_data, columns = ['City', 'Sales'])
            # results = all_data.groupby('City').sum()
            # st.bar_chart(all_data[results])
            # df.hist()
            # plt.show()
            # st.pyplot()

            results = all_data.groupby('City').sum()
            cities = [city for city, df in all_data.groupby('City')]

            plt.bar(cities, results['Sales'])
            plt.xticks(cities, rotation = 'vertical', size=8)
            plt.ylabel('Sales in USD')
            plt.xlabel('City name')
            plt.show()
            st.pyplot()


        if st.checkbox('Best hour'):
            st.write('Best time to show ads')
            hours = [hour for hour, df in all_data.groupby('Hour')]

            plt.plot(hours, all_data.groupby(['Hour']).count())
            plt.xticks(hours)
            plt.xlabel('Hours')
            plt.ylabel('Number of Orders')
            plt.grid()
            plt.show()
            st.pyplot()

        if st.checkbox('Best Pair'):
            st.write('Products often sold together')
            df = all_data[all_data['Order ID'].duplicated(keep=False)]

            df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

            df = df[['Order ID', 'Grouped']].drop_duplicates()
            from itertools import combinations
            from collections import Counter

            count = Counter()

            for row in df['Grouped']:
                row_list = row.split(',')
                count.update(Counter(combinations(row_list, 2)))

            for key, value in count.most_common(10):
                st.write(key, value)

        if st.checkbox('Most Sold'):
            st.write('Most sold product')
            product_group = all_data.groupby('Product')
            quantity_ordered = product_group.sum()['Quantity Ordered']

            products = [product for product, df in product_group]
            plt.bar(products, quantity_ordered)
            plt.ylabel('Quantity Ordered')
            plt.xlabel('Product')
            plt.xticks(products, rotation = 'vertical', size = 8)

            plt.show()
            st.pyplot()

if __name__ == '__main__':
    main()
