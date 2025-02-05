import streamlit as st
import analysis as an
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('Australia Car Market 🚗')

st.text('Please fill out this information to know more about the car you are looking for🙂')

Brand = st.selectbox('Brand👨🏻‍🔧',an.brands)

Model_array = np.sort(an.cars_df[an.cars_df['Brand'] == Brand]['Model'].unique())
Model= st.selectbox('Model🛠️',Model_array)

Variant_array = np.sort(an.cars_df[an.cars_df['Model'] == Model]['Variant'].unique())
Variant= st.selectbox('Variant🔧',Variant_array)


Year= st.slider('Year between: ⏱️',min_value=1995,max_value=2023,value=(2000,2010))
Kms= st.slider('Kilometers Between: 🛞',min_value=0,max_value=500000,value=(0,100000))


an.cars_df['Concatenate'] = an.cars_df['Brand'].astype(str) +' '+ an.cars_df['Model'].astype(str) +' '+ an.cars_df['Variant'].astype(str)

name_concatenate = Brand+' '+Model+ ' '+ Variant


df_filtered=an.cars_df[(an.cars_df['Concatenate']==name_concatenate) 
                        & (an.cars_df['Year'] >=Year[0])  & (an.cars_df['Year']<=Year[1]) 
                        & (an.cars_df['Kilometers'] >=Kms[0])  & (an.cars_df['Kilometers']<=Kms[1])]

st.dataframe(df_filtered[['Name','Variant','Year','Kilometers','Price','Gearbox','Fuel','Color']])

mean_price = round(df_filtered['Price'].mean(),0)
st.markdown(f"The average price of this vehicle is around **${mean_price:,.0f}**")

fig, ax = plt.subplots()
#plt.figure(figsize=(12,5))
ax = plt.hist(df_filtered['Price'],alpha=0.5)
st.pyplot(fig)


col1, col2 = st.columns(2)  # Two columns
col1.write("This is Column 1")
col2.write("This is Column 2")

st.sidebar.title("Sidebar Title")  # Adds a sidebar
st.sidebar.text_input("Enter something in the sidebar")
