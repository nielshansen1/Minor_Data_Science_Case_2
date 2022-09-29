#!/usr/bin/env python
# coding: utf-8

# ## Blog Assignment
# 
# For our project we want to merge the following three datasets:
# 
# - Netflix Originals Movies with IMDB scores 
# 
# - General Netflix Series / Movies data  (From this we want to add the rating column to our Dataframe)
# 
# - Netflix Stockprices 
# 
# With the merged Dataframe we'll do extensive data analysis with help from Pandas for data manipulation and Plotly to make interactive visualisations.
# Our goal is to discover if there is any corralation between the different features in this dataset. Examples of this can be corralation with movie releases and stock prices, IMDB scores and stock prices, rating and IMDB score.

# ### Using the Kaggle API to download the datasets we want to use during our project
# 
# The first step is to install the Kaggle library, and use it download the datasets.
# 
# - Documentation link: https://www.kaggle.com/docs/api
# - Code source: https://www.youtube.com/watch?v=DgGFhQmfxHo&t=331s

# In[1]:


# install the Kaggle library 
#!pip install kaggle


# Kaggle requires that the authentication key is present on our device ( using the following path: ~/.kaggle/kaggle.json), so we'll have to make a directory before we can proceed any futher

# In[2]:


# Try to import the Kaggle library. Before proceeding create the directory specified below, and place the kaggle.json there
#import kaggle


# In[3]:


# Try to import the Kaggle library again
#import kaggle


# In[4]:


# Import the Kaggle API from the Kaggle library
#from kaggle.api.kaggle_api_extended import KaggleApi


# In[5]:


# instantiate the API, then authenticate (uses the kaggle.json for login credentials)
#api = KaggleApi()
#api.authenticate()

#print("Succesfully connected to the Kaggle API!")


# In[6]:


# Use the Kaggle API to download the datasets we're using during the project
#api.dataset_download_file("luiscorter/netflix-original-films-imdb-scores",
#file_name="NetflixOriginals.csv")

#api.dataset_download_file("ariyoomotade/netflix-data-cleaning-analysis-and-visualization",
#file_name="netflix1.csv")

#api.dataset_download_file("akpmpr/updated-netflix-stock-price-all-time",
#file_name="netflix.csv")


# ### Dealing with encoded CSV files
# 
# Before we can proceed with loading the CSV files with Pandas there is one more step we need to take.
# The CSV files are encoded, and we'll use the chardet library to discover what type of encoding it is.
# After which we'll use the `encoding parameter` of Pandas to properly load the CSV file.

# In[7]:


# Import the needed library
import chardet

# Create a dict with file paths
files = {"NetflixOriginals.csv": "./data/NetflixOriginals.csv", "netflix.csv": "./data/netflix.csv", "netflix1.csv": "./data/netflix1.csv"}

# Loop through the dict, and print out the names and encoding type 
for name, file in files.items():
    with open(file, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))
    print(name, result)


# ### Loading in and Merging the Dataframes
# 
# Now we can start loading the datasets into Pandas with the `read_csv` function, and we will use the `merge` function to join the dataframes together.
# 
# - Note: It's only mandatory to use the encoding parameter for the Windows-1252 enconding, because Pandas doesn't have problems with loading in the other encoding formats

# In[8]:


# Import Pandas
import pandas as pd


# In[9]:


# Import the first dataset, and decode the csv file with Windows-1252 encoding
df = pd.read_csv("./data/NetflixOriginals.csv", encoding="Windows-1252")

# Change the column name of Premiere and set the format in DateTime to match the other dataset 
df.rename(columns = {"Premiere": "Date"}, inplace=True)
df.rename(columns = {"Title": "title"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])

# Show the first 5 rows
df.head()


# In[10]:


# Load in the second dataset
df2 = pd.read_csv("./data/netflix1.csv")

# Change the column name of title to match the other dataset
# df2.rename(columns = {"title": "Title"}, inplace=True)

# Show the first 5 rows
df2.head()


# In[11]:


# Load in the third dataset
df3 = pd.read_csv("./data/netflix.csv")

df3["Date"] = pd.to_datetime(df3["Date"])

# Show the first 5 rows
df3.head()


# When merging Dataframes there are multiple options on how to do it:
# 
# - Inner: keep all rows from both Dataframes that match (Which can result in dataloss in our case)
# 
# - Outer: keep all rows from both Dataframes (Which results in alot of rows with NaN values in our case)
# 
# - Left: Include all rows from Dataframe X and only those from y that match (X= target Dataframe, y= Dataframe to merge in)
# 
# - Right: Inculde all from Dataframe y and only those from X that match
# 
# We've made the the choice to use a Left Join, because Dataframe X is alot shorter then y

# In[12]:


# Create a new dataframe by merging df, df2, df3 on shared column names and using the Left Join
netflix_df = df.merge(df2[["title", "rating"]], on="title", how="left")         .merge(df3, on="Date", how="left") 
netflix_df.head()


# ## Data Cleaning

# In[13]:


# Check the number of rows and datatypes
netflix_df.info()


# In[14]:


# Check if there are NaN values
netflix_df.isna().sum()


# The Rating column and all the columns with Stock data have NaN values. We now have to decide what we want to do with the those rows, there are two main options for this: `pd.fillna` or `pd.dropna`. 
# 
# ##### Rating column
# For the Rating column we have decided to fill all NaN values with U for unknown, because 80 rows would be alot of data to discard.
# 
# ##### Stock data columns
# For the Stock data columns we've tried to apply the `pd.interpolate` function, but it wasn't succesfull . We've decided to drop the rows in question, because dropping 36 rows could be better justified

# In[15]:


# Sort all values in the Dataframe by date, to order the data first
netflix_df.sort_values("Date", inplace=True)

# Fill the NaN values of the rating column with U 
netflix_df["rating"].fillna("U", inplace=True)

# Drop all rows with NaN values
netflix_df.dropna(inplace=True)


# In[16]:


# Check the number of rows and datatypes again
netflix_df.info()


# In[17]:


# Check the number of NaN values again
netflix_df.isna().sum()


# In[18]:


# Show the first 5 rows
netflix_df.head()


# ## Streamlit: schrijven van de app

# In[19]:


#install the Streamlit library and import it
#!pip install streamlit
import streamlit as st


# In[20]:


# Titel van de app
st.title("The effect of Netflix movie IMDB scores on Netflix' stock")


# In[21]:


st.text_area("Inleiding",
            '''For our project we want to merge the following three datasets:

            - Netflix Originals Movies with IMDB scores 

            - General Netflix Series / Movies data  (From this we want 
            to add the rating column to our Dataframe)

            - Netflix Stockprices 

            With the merged Dataframe we'll do extensive data analysis 
            with help from Pandas for data manipulation and Plotly to make
            interactive visualisations.
            Our goal is to discover if there is any corralation between
            the different features in this dataset. Examples of this can
            be corralation with movie releases and stock prices, IMDB scores
            and stock prices, rating and IMDB score. ''', )


# In[22]:


# Maak een streamlit dataframe zodat hij weergeven wordt op de app
st_netflix_df = st.dataframe(netflix_df)


# In[32]:


import plotly.express as px
fig = px.bar(netflix_df , x='Genre')
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(width=1000, height=1000)


st.plotly_chart(fig)
fig.show()


# In[26]:


# Create a exchange rate difference column, to with the difference between the High and Low points of the day
netflix_df["Daily exchange rate difference"] = netflix_df["Open"] - netflix_df["Close"]

# Show the first 5 rows
netflix_df.head()


# In[31]:


fig = px.line(netflix_df, 
              x="Date", 
              y="Daily exchange rate difference", 
              hover_name="title")
st.plotly_chart(fig)
fig.show()


# In[33]:


fig = px.scatter(netflix_df, 
                x="IMDB Score", 
                y="Daily exchange rate difference",
                color="Genre")
st.plotly_chart(fig)
fig.show()


# In[30]:


from turtle import color
import plotly.graph_objects as go

imdb_top20 = netflix_df.sort_values(['IMDB Score'], ascending=False)[0:20]

labels = imdb_top20["Genre"]
values = imdb_top20["IMDB Score"]
colours = px.colors.sequential.Aggrnyl

fig = go.Figure()
fig.add_trace(go.Pie(labels=labels, 
                     values=values, 
                     pull=[0.2, 0, 0.3, 0],
                     marker= {'colors' : colours}))
fig.update_layout(title="Top 20 IMDB Scores distribution")
st.plotly_chart(fig)
fig.show()


# In[34]:


fig = px.bar(imdb_top20, 
             x="IMDB Score",
             y="title",
             color="Genre",
             title="Top 20 IMDB Scores")
st.plotly_chart(fig)
fig.show()


# In[35]:


rating_buttons = [{'label': "All", 'method': "update", 'args': [{"visible": [True, True, True, True, True, True, True, True, True, True]},{'title':'All'}]},
             {'label': "TV-14", 'method': "update", 'args': [{"visible": [True, False, False, False, False, False, False, False, False, False]},{'title':'TV-14'}]},
             {'label': "TV-MA", 'method': "update", 'args': [{"visible": [False, True, False, False, False, False, False, False, False, False]},{'title':'TV-MA'}]},
             {'label': "TV-PG", 'method': "update", 'args': [{"visible": [False, False, True, False, False, False, False, False, False, False]},{'title':'TV-PG'}]},
             {'label': "U", 'method': "update", 'args': [{"visible": [False, False, False, True, False, False, False, False, False, False]},{'title':'U'}]},
             {'label': "TV-G", 'method': "update", 'args': [{"visible": [False, False, False, False, True, False, False, False, False, False]},{'title':'TV-G'}]},
             {'label': "PG-13", 'method': "update", 'args': [{"visible": [False, False, False, False, False, True, False, False, False, False]},{'title':'PG-13'}]},
             {'label': "R", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, True, False, False, False]},{'title':'R'}]},
             {'label': "TV-Y", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, True, False, False]},{'title':'TV-Y'}]},
             {'label': "TV-Y7", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, True, False]},{'title':'TV-Y7'}]},
             {'label': "PG", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, True]},{'title':'PG'}]}]

fig = px.scatter(data_frame=netflix_df, x='Date', y='IMDB Score', color='rating')
fig.update_layout({'updatemenus':[{'type': 'dropdown','x': 1.3,'y': 1,'showactive': True,'active': 0,'buttons': rating_buttons}]})
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig)
fig.show()


# In[ ]:




