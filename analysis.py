# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import geopandas as gpd
import seaborn as sns


# %% [markdown]
# ##First approach to the dataframe

# %%
cars_df = pd.read_csv(r'C:\Users\pipec\OneDrive\Documentos\Python Scripts\Australia Car Market Data\cars_info.csv')
cars_df.head()


# %%
print(cars_df.describe())
print(cars_df.dtypes)

print(len(cars_df))



# %% [markdown]
# ##Finding the top 5 of the most sold car Brands

# %%
#Top 5 of the most sold car Brands.

cars_dups = cars_df['Brand'].value_counts()

most_cars_sold = cars_dups.sort_values(ascending=False).head(5)

print(most_cars_sold)
plt.bar(most_cars_sold.index,most_cars_sold.values)
#plt.xticks(rotation=80)

for i, value in enumerate(most_cars_sold.values):
    plt.text(i, value + 5, str(value), ha='center', va='bottom')

plt.xlabel('Brand of vehicle')
plt.ylabel('Number of purchases')
plt.title('Top 5 of brands cars sold in Australia')
plt.show()

##Now let's focus on Toyota.

Toyota_cars = cars_df[cars_df['Brand'] == 'Toyota']['Model'].value_counts()
print(Toyota_cars.describe())

##Filtering models according to second quartile = 9
Toyota_cars = Toyota_cars[Toyota_cars.values >9]
print(Toyota_cars)
##Plotting Toyota cars by models
plt.bar(Toyota_cars.index,Toyota_cars.values)
plt.xticks(rotation=80)

for i, value in enumerate(Toyota_cars.values):
    plt.text(i, value + 5, str(value), ha='center', va='bottom')

plt.xlabel('Model of vehicle')
plt.ylabel('Number of purchases')
plt.title('Models of Toyota cars sold in Australia')
plt.show()



# %% [markdown]
# ##Comparing variation of each specific vehicle.

# %%

##defining a function where we can analyze an specific vehicle.
def vehicle_variation(name):
    plt.boxplot(cars_df[cars_df['Name'] == name]['Price'])
    plt.xticks([1],[name])
    plt.xlabel('Vehicle Name')
    plt.ylabel('Price')
    plt.title('Boxplot of Vehicle Prices')
    plt.show()

vehicle_variation('2010 Mercedes-Benz E250 CDI Avantgarde 207')


# %% [markdown]
# Now le'ts check which continent is the king in Australia.
# I wan to agroup the brands per continents and then plot a warm graph.

# %%
##Agrouping Brands per continent.

# List of brands
brands = ['Toyota', 'Mercedes-Benz', 'Holden', 'Nissan', 'Ford', 'BMW', 'Isuzu', 'Hyundai',
          'Volkswagen', 'Lexus', 'Mazda', 'Audi', 'Subaru', 'Mitsubishi', 'Kia', 'Skoda',
          'Renault', 'Porsche', 'Jeep', 'Honda', 'Ssangyong', 'Volvo', 'Land Rover', 'MG',
          'Suzuki', 'Ram', 'Mini', 'Jaguar', 'LDV', 'HSV', 'Alfa Romeo', 'Aston Martin',
          'Hino', 'Chrysler', 'Citroen', 'Infiniti', 'Peugeot', 'Chevrolet',
          'Lamborghini', 'Fiat', 'Bentley', 'Dodge', 'Haval', 'Great Wall', 'Abarth',
          'Foton', 'Genesis', 'GWM', 'FPV', 'Mitsubishi Fuso', 'Maserati', 'Iveco',
          'Mahindra', 'Opel', 'Saab', 'Chery', 'Smart', 'Proton', 'Cupra']

# Continents for each brand based on origin
continents = ['Asia', 'Europe', 'Oceania', 'Asia', 'North America', 'Europe', 'Asia', 'Asia',
              'Europe', 'Asia', 'Asia', 'Europe', 'Asia', 'Asia', 'Asia', 'Europe',
              'Europe', 'Europe', 'North America', 'Asia', 'Asia', 'Europe', 'Europe', 'Asia',
              'Asia', 'North America', 'Europe', 'Europe', 'Asia', 'Oceania', 'Europe', 'Europe',
              'Asia', 'North America', 'Europe', 'Asia', 'Europe', 'North America',
              'Europe', 'Europe', 'Europe', 'North America', 'Asia', 'Asia', 'Europe',
              'Asia', 'Asia', 'Asia', 'Asia', 'Europe', 'Europe', 'Asia',
              'Asia', 'Europe', 'Europe', 'Asia', 'Asia', 'Asia', 'Europe']

# Create DataFrame
brands_df = pd.DataFrame({'Brand': brands, 'Continent': continents})
brands_df

merge_df = pd.merge(cars_df[['Brand','Price']],brands_df,how='left')
merge_df

merge_df_count = merge_df['Continent'].value_counts()
merge_df_count

#print(max(merge_df_count.values))


# %% [markdown]
# #Now let's check how the kms affect the price.

# %%
#Plotting kms vs price
continents_unique = brands_df['Continent'].unique()
kms_price = pd.merge(cars_df,brands_df,how='inner')
kms_price

#I've realized that there is an outlier not typical of a car with more than 2 million of kms. I will adjust those kms cause doesn't make sense.
plt.figure(figsize=(12,5))
for i in continents_unique:
    kms_price_i = kms_price[(kms_price['Continent'] == i) & (kms_price['Kilometers'] <= 1000000)][['Kilometers','Price']]
    #print(kms_price)
    plt.scatter(kms_price_i['Kilometers'],kms_price_i['Price'],s=10,label=i)
plt.legend()
plt.xlabel('Kilometers')
plt.ylabel('Price')
plt.show()

#print(brands_df)

# %%
print(cars_df[cars_df['Kilometers']  > 900000])

# %%
plt.figure(figsize=(13,5))

color = ['blue','green','orange','red']
for i in range(1,5):
    
    c=continents_unique[i-1]
    plt.subplot(2,2,i)
    kms_price_i = kms_price[(kms_price['Continent'] == c) & (kms_price['Kilometers'] <= 1000000)][['Kilometers','Price']]
    plt.scatter(kms_price_i['Kilometers'],kms_price_i['Price'],s=8,c=color[i-1])
    plt.axvline(x=400000, color='yellow', linestyle='--')
    plt.axhline(y=150000, color='green', linestyle='--')
    plt.xlim(0,800000)
    #plt.ylim(0,1000000)
    plt.title(str(c)+' Continent kms VS Price')
    plt.subplots_adjust(hspace=0.6)

plt.show()




# %% [markdown]
# The graph above shows the variation in terms of price and mileage according to each brands' continent.
# Asian brands experiment wide high kilometers and their prices in most of the cases not exceeding $200.000. On the other hand the European brands show the opposite trend with a very low kilometers and prices higher than $500.000. The other two continents in mention show a similar behaviour.
# 
# 

# %% [markdown]
# Now, lets have a look on the next hipotesis:
# Usually the cars with a mecanic gearbox is cheaper than cars with automatic gearbox:
# Ho: The gearbox type has no effect on car price. (The average price of manual and automatic cars is the same.)
# H1:  The gearbox type does affect car price. (The average prices are different.)

# %%
from scipy.stats import iqr
#Cleaning and Separating the data

price_auto= cars_df[cars_df['Gearbox']=='Automatic']['Price']
price_manual= cars_df[cars_df['Gearbox']=='Manual']['Price']

#plotting box plots of each gearbox type

x = [price_manual,price_auto]
plt.boxplot(x,labels=['Manual Gearbox','Automatic Gearbox'])
plt.show()

#According to the graph above we need to remove outliers. I'll use the IQR method to do that.
IQR_auto = iqr(price_auto)
Q1_auto = np.quantile(price_auto,0.25)
Q3_auto = np.quantile(price_auto,0.75)

IQR_manual = iqr(price_manual)
Q1_manual = np.quantile(price_manual,0.25)
Q3_manual = np.quantile(price_manual,0.75)

print('Automatic Gearbox: IQR = '+ str(IQR_auto)+ ', Q1= '+str(Q1_auto)+ ', Q3= '+str(Q3_auto))
print('Manual Gearbox: IQR = '+ str(IQR_manual)+ ', Q1= '+str(Q1_manual)+ ', Q3= '+str(Q3_manual))

#Setting limits to remove outliers according to the IQR:
top_limit_auto= Q3_auto + 1.5*IQR_auto
botton_limit_auto= Q1_auto - 1.5*IQR_auto

top_limit_manual= Q3_manual + 1.5*IQR_manual
botton_limit_manual= Q1_manual - 1.5*IQR_manual
#Redefining data again
price_auto= cars_df[(cars_df['Gearbox']=='Automatic')& (cars_df['Price'] <=top_limit_auto) & (cars_df['Price'] >= botton_limit_auto)]['Price']
price_manual= cars_df[(cars_df['Gearbox']=='Manual')& (cars_df['Price'] <=top_limit_manual) & (cars_df['Price'] >= botton_limit_manual)]['Price']

#Now, let's plot again our boxplot :)
x = [price_manual,price_auto]
plt.boxplot(x,labels=['Manual Gearbox','Automatic Gearbox'])
plt.show()

#plotting histograms of each gearboxtype
plt.hist(price_auto,alpha = 0.6,label='Automatic Gearbox')
plt.hist(price_manual, alpha = 0.6,label='Manual Gearbox')
plt.legend()
plt.show() #We can see the significant difference between automatic and manual gearboxes.

#checking assumptions to test Ho.

from scipy.stats import shapiro, levene

# Normality test (Shapiro-Wilk)
print("Shapiro Test (Manual):", shapiro(price_manual))
print("Shapiro Test (Automatic):", shapiro(price_auto))

# Variance test (Levene's Test)
print("Levene's Test:", levene(price_manual, price_auto)) #The Shapiro test said the distributions are not normal and the variances of each dataset is not the same (p-value < 0.05)

#According to these results, the Mann-Whitney U test sounds suitable to test our Ho.
from scipy.stats import mannwhitneyu

u_statistic, p_value = mannwhitneyu(price_manual, price_auto, alternative='two-sided')

# Print the results
print(f"Mann-Whitney U Statistic: {u_statistic}")
print(f"P-value: {p_value}")

# Interpretation
if p_value < 0.05:
    print("The difference in prices between manual and automatic cars is statistically significant so we can reject the null hypothesis.")
else:
    print("There is no statistically significant difference in prices between manual and automatic cars.")

#In conclusion, There is strong evidence to confirm that the gearbox type affect the price of every car.


# %%
#Now let's check what is the top 3 colors vehicle in Australia
colors_standard=cars_df['Color'].str.capitalize() #Capitalizing all values to don't lose info ('Blue','blue','BLUE')
colors_df = colors_standard.value_counts().head(10)
print(colors_df)

sum = 0
for i in colors_df.values:
    sum = sum + i

# Create a dictionary mapping color names to actual colors
color_map = {
    'White': 'white',
    'Black': 'black',
    'Blue': 'blue',
    'Red': 'red',
    'Green': 'green',
    'Gold': 'gold',
    'Gray': 'gray',
    'Silver': 'silver',
    'Grey': 'grey',
    'Orange': 'orange',
    'Brown': 'brown'
}

# Generate a list of colors for the bars based on the dataset's color names
bar_colors = [color_map.get(color, 'gray') for color in colors_df.index]  # Default to gray if color is missing


plt.figure(figsize=(11,7))
ax = sns.barplot(
    x=colors_df.values, 
    y=colors_df.index, 
    palette= bar_colors, 
    edgecolor="black"
)
for i, value in enumerate(colors_df.values):
    ax.text(value + 0.5, i, str(round(value/sum*100,2))+'%', color='black', va='center', fontsize=10)


ax.set_xticks([])
plt.xlabel("Percentage")
plt.ylabel("Car Color")
plt.title("Distribution of Car Colors")
plt.show()




