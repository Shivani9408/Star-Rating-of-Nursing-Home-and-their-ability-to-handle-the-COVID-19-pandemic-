#!/usr/bin/env python
# coding: utf-8

# 
#                 
#  DATA ANALYSIS OF  HOW THE STAR RATING OF A FACILITY REFLECTS THEIR BILITY TO RESPOND TO THE COVID-19 PANDEMIC
#  
#                 
#  
#  Import the packages

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 


# 
# Read the Nursing Home COVID Data and Nursing Home Star Comparisons csv files

# In[9]:


nursing_home_COVID19_data = pd.read_csv('COVID-19_Nursing_Home_Dataset.csv')
star_ratings = pd.read_csv('Star_Ratings.csv')


# In[5]:


nursing_home_COVID19_data.info()


# In[6]:


nursing_home_COVID19_data.head(5)


# In[7]:


star_ratings.info()


# In[8]:


star_ratings.head(5)


# Joined the above mentioned datasets on Federal Provider number using Inner Join 

# In[24]:


merged_data = pd.merge(nursing_home_COVID19_data,star_ratings, on = ['Federal Provider Number'],how = 'inner')


# In[25]:


merged_data.shape


# In this i have removed the NA values from the dataset which are more than 30 percent

# In[26]:


filtered_data = merged_data[[column for column in merged_data if merged_data[column].count()/len(merged_data)>=0.3]]
filtered_data.shape


# The below piece of code will help to know which columns have been dropped 
# or we can say the columns having null values more than 30 percent

# In[27]:


print("List of dropped Columns: ", end = " ")
for c in merged_data.columns:
    if c not in filtered_data.columns:
        print(c,end = ", ")
print("\n")
merged_data = filtered_data


# Remove the duplicates from the dataset

# In[30]:


sum(filtered_data.duplicated())


# In[36]:


correlation_matrix = filtered_data.corr()
f, ax = plt.subplots(figsize = (12,12))
sns.heatmap(correlation_matrix, ax = ax, cmap ="RdBu",linewidths = 0.1)


# In[120]:


filtered_data=filtered_data[filtered_data['Submitted Data']=='Y']


# The below table denotes the Total Confirmed COVID-19 cases in United States 

# In[121]:


x=filtered_data.groupby('Provider State_x',sort=True)['Residents Total Confirmed COVID-19'].sum() 
df = pd.DataFrame(x).reset_index()
df.columns = ['State', 'Total Confirmed COVID-19 cases']
df


# The below bar chart denotes the count of Total Confirmed cases in every state of US 

# In[122]:


def plotdata(x_axis,y_axis,x_label,title,y_label):
    data1=filtered_data.groupby(x_axis,sort=True)[y_axis].sum()
    ax = data1.plot(kind='bar', figsize=(14,8), color="indigo", fontsize=13);
    ax.set_alpha(0.8)
    ax.set_title(title, fontsize=25)
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    return plt.show()


# In[123]:


plotdata('Provider State_x', 'Residents Total Confirmed COVID-19', 'Provider State', 'Total Cases', 'Confirmed Cases')


# The below bar chart denotes the count of Total Deaths in every state of US

# In[124]:


plotdata('Provider State_x','Residents Total COVID-19 Deaths','Provider State','Total Death per state','Total number of Death')


# Here i have calculated the count of Total Confirmed COVID-cases as per the Provider name, state and city  as shown in the table below

# In[200]:


s=filtered_data.groupby(['Provider State_x','Provider City','Provider Name_x'],sort=True)['Residents Total Confirmed COVID-19'].sum().sort_values(ascending=False)
nursinghome_cases=pd.DataFrame(s).reset_index()
nursinghome_cases=pd.DataFrame(s.nlargest(10)).reset_index()
nursinghome_cases.columns=['Provider State_x','Provider City','Provider Name_x','Total Confirmed cases']
nursinghome_cases


# In[201]:


ax = nursinghome_cases[['Provider Name_x','Total Confirmed cases']].plot(kind='bar', title = "Nursing Home with highest number of COVID-19 cases", color="maroon",figsize=(8, 10), legend=True, fontsize=12)
ax.set_xlabel("Providers name ", fontsize=12)
ax.set_ylabel("Confirmed cases", fontsize=12)
plt.show()


# Here i have calculated the count of Total deaths due to COVID-19 as per the Provider name, state and city  as shown in the table below

# In[202]:


s=filtered_data.groupby(['Provider State_x','Provider City','Provider Name_x'],sort=True)['Residents Total COVID-19 Deaths'].sum().sort_values(ascending=False)
nursinghome_deaths=pd.DataFrame(s).reset_index()
nursinghome_deaths=pd.DataFrame(s.nlargest(10)).reset_index()
nursinghome_deaths.columns=['Provider State_x','Provider City','Provider Name_x','Total deaths']
nursinghome_deaths


# In[203]:


ax = nursinghome_deaths[['Provider Name_x','Total deaths']].plot(kind='bar', title = "Nursing Home with highest number of COVID-19 deaths", color="maroon",figsize=(8, 10), legend=True, fontsize=12)
ax.set_xlabel("Providers name ", fontsize=12)
ax.set_ylabel("Total deaths", fontsize=12)
plt.show()


# Calcualted the count of amenties in the nursing home  faced highest number of deaths as shown in the table below

# In[210]:


check_amenities=nursinghome_deaths.merge(filtered_data,on=['Provider Name_x'],how='inner')


# In[227]:


check_data =nursinghome_deaths.merge(filtered_data,on=['Provider Name_x'],how='inner')
value =check_data[['Provider Name_x','Shortage of Aides','Shortage of Clinical Staff',
               'One-Week Supply of Hand Sanitizer','One-Week Supply of Gowns','One-Week Supply of Gloves'
                ]].groupby('Provider Name_x')


# In[228]:


value.describe()


# QM Rating, RN Staffing Rating and Staffing Rating of the Nursing home faced the most COVID-19 deaths 

# In[242]:


res = (check_amenities.loc[:, ['Provider Name_x','QM Rating', 'RN Staffing Rating', 'Staffing Rating']]).groupby("Provider Name_x")
res.describe()


# After analyzing the two datasets which is Nursing Home COVID Data and Nursing Home Star Comparisons, 
# the insights i found are mentioned below:
# Considering,CEDARBROOK SENIOR CARE AND REHABILITATION Nursing home, the total number of COVID-19 Confirmed cases 
# admitted were 1800 and the COVID-19 deaths faced by the nursing home was 709, which means approx.40% of the patients died from COVID-19. This moves the attention towards the available supplies of the hospital and after analyzing we can say that it has shortage of PPE such as hand sanitizer, gowns and gloves.
# Despite having good QM rating, nursing home was not prepared to handle the COVID-19 cases as it has lack of medical supplies and among all the nursing homes in the United States it faced 3rd highest deaths.
# As per the analysis,it shows that nursing home has lack of PPE for the staff which might have exposed them to the virus as well.
# Overall, we can infer that nursing homes doesn't have enough medical supplies to handle COVID-19 situation as this noval virus requires the sanitery measures the most.

# In[ ]:




