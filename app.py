import streamlit as st
import analysis as an
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import seaborn as sns
import streamlit.components.v1 as components



st.title('Australia Car Market 🚗')

st.text('Complete this form to learn more about the car you are looking for. 🙂')

#Creating the form
Brand = st.selectbox('Brand 👨🏻‍🔧',sorted(an.brands),index=56) #Brand input

Model_array = np.sort(an.cars_df[an.cars_df['Brand'] == Brand]['Model'].unique())
Model= st.selectbox('Model 🛠️',Model_array) #Model input

Variant_array = 'Select all variants'
Variant_array = np.append(Variant_array,np.sort(an.cars_df[an.cars_df['Model'] == Model]['Variant'].unique()))
Variant= st.selectbox('Variant 🔧',Variant_array) #Variant input

Gearbox = st.radio('Select Gearbox: ',['Automatic','Manual',"I don't mind"],index=2) #Gearbox input

Year= st.slider('Year range: ⏱️',min_value=1995,max_value=2023,value=(2000,2020)) #Year input
Kms= st.slider('Kilometers range: 🛞',min_value=0,max_value=500000,value=(0,150000),step=10000) #kilometers input

st.markdown(
    """
    ---
 
    """
)

st.title('Your results 📋')

#Creating concatenate strings as 'Primary key' so we can match the primary key with the options the user chose.
if Variant == 'Select all variants':
    if Gearbox == "I don't mind":
        an.cars_df['Concatenate'] = an.cars_df['Brand'].astype(str) +' '+ an.cars_df['Model'].astype(str) 
        name_concatenate = Brand+' '+Model
    else :
        an.cars_df['Concatenate'] = an.cars_df['Brand'].astype(str) +' '+ an.cars_df['Model'].astype(str) +' '+ an.cars_df['Gearbox'].astype(str)
        name_concatenate = Brand+' '+Model+' '+ Gearbox
elif Gearbox == "I don't mind":
    an.cars_df['Concatenate'] = an.cars_df['Brand'].astype(str) +' '+ an.cars_df['Model'].astype(str) +' '+ an.cars_df['Variant'].astype(str)
    name_concatenate = Brand+' '+Model+' '+ Variant    
else:
    an.cars_df['Concatenate'] = an.cars_df['Brand'].astype(str) +' '+ an.cars_df['Model'].astype(str) +' '+ an.cars_df['Variant'].astype(str)  +' '+ an.cars_df['Gearbox'].astype(str)
    name_concatenate = Brand+' '+Model+' '+ Variant+' '+ Gearbox


#Displaying the dataframe
df_filtered=an.cars_df[(an.cars_df['Concatenate']==name_concatenate) 
                        & (an.cars_df['Year'] >=Year[0])  & (an.cars_df['Year']<=Year[1]) 
                        & (an.cars_df['Kilometers'] >=Kms[0])  & (an.cars_df['Kilometers']<=Kms[1])]

st.dataframe(df_filtered[['Name','Year','Kilometers','Price','Type','Color','Gearbox','Fuel']],hide_index=True)

mean_price = round(df_filtered['Price'].mean(),0)

if  pd.isna(mean_price):
    st.markdown('No cars found.')
else:
    st.subheader(f'The average price of this vehicle is **${mean_price:,.0f}** .') #Showing average price


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
    r2 = float(r_value**2)
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
    📉 The line shows the general trend as a linear regression with **R² = {r2:,.2f}**.",unsafe_allow_html=True)
except:
    st.text('')

st.markdown(
    """
    ---
 
    """
)
st.subheader(f'Would you like to know more about vehicles sold in Australia? .')
st.markdown(f'Feel free to explore this descriptive analysis dashboard by clicking on the following link: [**click here**](https://public.tableau.com/views/Dashboard_Australia_Car_Market/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)  \
            or kindly see this brief overview.')

#Embeding dashboard made in tableau public:
tableau_URL= """ <div class='tableauPlaceholder' id='viz1741836299623' style='position: relative'><noscript><a href='#'><img alt='Australian Car Market Overview ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Da&#47;Dashboard_Australia_Car_Market&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Dashboard_Australia_Car_Market&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Da&#47;Dashboard_Australia_Car_Market&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1741836299623');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='757px';vizElement.style.height='1127px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='757px';vizElement.style.height='1127px';} else { vizElement.style.width='100%';vizElement.style.height='1777px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
"""

# Embed using the HTML iframe method
components.html(tableau_URL, height=1200)


# Footnote

st.markdown(
    """
    ---
    Made with passion❤️‍🔥  
    For more information, visit the [Australia Car Market Database](https://www.kaggle.com/datasets/lainguyn123/australia-car-market-data). 
    """
)
st.markdown('Created by **Andres Cardenas**, visit my [linkedin profile](https://www.linkedin.com/in/andr%C3%A9s-c%C3%A1rdenas-4b992a191/) .')
