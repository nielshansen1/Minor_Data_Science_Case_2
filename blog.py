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

# Kaggle requires that the authentication key is present on our device ( using the following path: ~/.kaggle/kaggle.json), so we'll have to make a directory before we can proceed any futher

# ## Streamlit

# In[3]:


#install the Streamlit library and import it
#!pip install streamlit
import streamlit as st


# In[ ]:


st.title("DIT IS EEN TEST")


# ### Dealing with encoded CSV files
# 
# Before we can proceed with loading the CSV files with Pandas there is one more step we need to take.
# The CSV files are encoded, and we'll use the chardet library to discover what type of encoding it is.
# After which we'll use the `encoding parameter` of Pandas to properly load the CSV file.

# In[4]:


# Import the needed library
#get_ipython().system('pip install chardet')
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

# In[127]:


# Import Pandas
import pandas as pd


# In[151]:


# Import the first dataset, and decode the csv file with Windows-1252 encoding
df = pd.read_csv("./data/NetflixOriginals.csv", encoding="Windows-1252")

# Change the column name of Premiere and set the format in DateTime to match the other dataset 
df.rename(columns = {"Premiere": "Date"}, inplace=True)
df.rename(columns = {"Title": "title"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])

# Show the first 5 rows
df.head()


# In[152]:


# Load in the second dataset
df2 = pd.read_csv("./data/netflix1.csv")

# Change the column name of title to match the other dataset
# df2.rename(columns = {"title": "Title"}, inplace=True)

# Show the first 5 rows
df2.head()


# In[153]:


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

# In[154]:


# Create a new dataframe by merging df, df2, df3 on shared column names and using the Left Join
netflix_df = df.merge(df2[["title", "rating"]], on="title", how="left")         .merge(df3, on="Date", how="left") 
netflix_df.head()


# ## Data Cleaning

# In[155]:


# Check the number of rows and datatypes
netflix_df.info()


# In[156]:


# Check if there are NaN values
netflix_df.isna().sum()


# The Rating column and all the columns with Stock data have NaN values. We now have to decide what we want to do with the those rows, there are two main options for this: `pd.fillna` or `pd.dropna`. 
# 
# ##### Rating column
# For the Rating column we have decided to fill all NaN values with U for unknown, because 80 rows would be alot of data to discard.
# 
# ##### Stock data columns
# For the Stock data columns we've tried to apply the `pd.interpolate` function, but it wasn't succesfull . We've decided to drop the rows in question, because dropping 36 rows could be better justified

# In[162]:


# Sort all values in the Dataframe by date, to order the data first
netflix_df.sort_values("Date", inplace=True)

# Fill the NaN values of the rating column with U 
netflix_df["rating"].fillna("U", inplace=True)

# Drop all rows with NaN values
netflix_df.dropna(inplace=True)


# In[165]:


# Check the number of rows and datatypes again
netflix_df.info()


# In[163]:


# Check the number of NaN values again
netflix_df.isna().sum()


# In[164]:


# Show the first 5 rows
netflix_df.head()

