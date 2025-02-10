import streamlit as st
import analysis as an
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import seaborn as sns


st.title('Australia Car Market 🚗')

st.text('Complete this form to learn more about the car you are looking for. 🙂')

Brand = st.selectbox('Brand 👨🏻‍🔧',an.brands)

Model_array = np.sort(an.cars_df[an.cars_df['Brand'] == Brand]['Model'].unique())
Model= st.selectbox('Model 🛠️',Model_array)


Variant_array = 'Select all variants'
Variant_array = np.append(Variant_array,np.sort(an.cars_df[an.cars_df['Model'] == Model]['Variant'].unique()))
Variant= st.selectbox('Variant 🔧',Variant_array)


Year= st.slider('Year between: ⏱️',min_value=1995,max_value=2023,value=(2000,2010))
Kms= st.slider('Kilometers Between: 🛞',min_value=0,max_value=500000,value=(0,100000))



if Variant == 'Select all variants':
    an.cars_df['Concatenate'] = an.cars_df['Brand'].astype(str) +' '+ an.cars_df['Model'].astype(str)
    name_concatenate = Brand+' '+Model
else:
    an.cars_df['Concatenate'] = an.cars_df['Brand'].astype(str) +' '+ an.cars_df['Model'].astype(str) +' '+ an.cars_df['Variant'].astype(str)
    name_concatenate = Brand+' '+Model+ ' '+ Variant


df_filtered=an.cars_df[(an.cars_df['Concatenate']==name_concatenate) 
                        & (an.cars_df['Year'] >=Year[0])  & (an.cars_df['Year']<=Year[1]) 
                        & (an.cars_df['Kilometers'] >=Kms[0])  & (an.cars_df['Kilometers']<=Kms[1])]

st.dataframe(df_filtered[['Name','Year','Kilometers','Price','Type','Color','Gearbox','Fuel']],hide_index=True)

mean_price = round(df_filtered['Price'].mean(),0)

if  pd.isna(mean_price):
    st.markdown('No cars found.')
else:
    st.markdown(f"The average price of this vehicle is around **${mean_price:,.0f}**")


fig1  = plt.figure(figsize=(12, 6))
##Plotting histogram prices

sns.histplot(df_filtered['Price'], stat='density', color='skyblue')
sns.kdeplot(df_filtered['Price'], color='red', linewidth=2.5)

plt.xlabel('Price ($AUD)')
plt.ylabel('Count')
plt.title('1.) ' + str(name_concatenate) +' Histogram Price')

st.pyplot(fig1)

st.markdown(f"🚗 This first graph shows how much people are paying for **{str(name_concatenate)}** cars.<br> \
📶 The blue bars represent **the number of cars** in different **price ranges**. <br> \
📉 The red curve is a smooth line showing the general trend, like a **“best guess”** of where prices are **most common**.",unsafe_allow_html=True)

#Plotting linear regression
fig2  = plt.figure(figsize=(12, 6))
plt.scatter(df_filtered['Kilometers'],df_filtered['Price'],s=22)

try:
    slope, intercept, r_value, p_value, std_err = linregress(df_filtered['Kilometers'], df_filtered['Price'])  # 1 = linear regression (degree 1)
    regression_line = slope * df_filtered['Kilometers'] + intercept
    plt.plot(df_filtered['Kilometers'], regression_line, color="red", label=f"Regression Line (y={slope:.2f}x+{intercept:.2f})")  # Linear regression
except:
    st.text('Please try again.')

plt.xlabel('Kilometers')

plt.ticklabel_format(style='plain', axis='x')
plt.ylabel('Price ($AUD)')
plt.title('2.) '+ str(name_concatenate) + ' Kilometers VS Price')
plt.legend()

st.pyplot(fig2)
try:
    st.markdown(f"🚗 This second graph shows a trend of the **{str(name_concatenate)}** price.<br> \
    📶 Each dot represents a specific car. <br> \
    📉 The line shows the general trend as a linear regression with **R = {r_value:,.2f}**.",unsafe_allow_html=True)
except:
    st.text('')


# Footnote
st.markdown(
    """
    ---
    Made with passion❤️‍🔥  
    Created by Andres Cardenas, visit my [linkedin profile](https://www.linkedin.com/in/andr%C3%A9s-c%C3%A1rdenas-4b992a191/) . 
    """
)



#st.sidebar.title("Sidebar Title")  # Adds a sidebar
#st.sidebar.text_input("Enter something in the sidebar")
