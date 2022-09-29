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
import streamlit as st


# In[20]:


# Titel van de app
st.title("The effect of Netflix movie IMDB scores on Netflix' stock")


# In[21]:


st.header('Introduction')


# In[22]:


st.text('''For our project we want to merge the following three datasets:

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
            and stock prices, rating and IMDB score. ''')


# In[23]:


st.header('Using the Kaggle API to download the datasets we want to use during our project')


# In[24]:


st.text('''The first step is to install the Kaggle library, and use it download the datasets.

            - Documentation link: https://www.kaggle.com/docs/api
            - Code source: https://www.youtube.com/watch?v=DgGFhQmfxHo&t=331s
        ''')


# In[25]:


code = '''#install the Kaggle library 
          !pip install kaggle'''
st.code(code, language="python")


# In[26]:


st.text('''Kaggle requires that the authentication key is present on our device 
( using the following path: ~/.kaggle/kaggle.json), so we'll have to make a
directory before we can proceed any futher.
''')


# In[27]:


code = '''# Import the Kaggle API from the Kaggle library
from kaggle.api.kaggle_api_extended import KaggleApi
            
# instantiate the API, then authenticate (uses the kaggle.json for login credentials)
api = KaggleApi()
api.authenticate()
print("Succesfully connected to the Kaggle API!")
          
# Use the Kaggle API to download the datasets we're using during the project
api.dataset_download_file("luiscorter/netflix-original-films-imdb-scores",
file_name="NetflixOriginals.csv")

api.dataset_download_file("ariyoomotade/netflix-data-cleaning-analysis-and-visualization",
file_name="netflix1.csv")

api.dataset_download_file("akpmpr/updated-netflix-stock-price-all-time",
file_name="netflix.csv")'''
st.code(code, language='python')


# In[28]:


st.header('Dealing with encoded CSV files')


# In[29]:


st.text('''Before we can proceed with loading the CSV files with Pandas there is one more step
we need to take. The CSV files are encoded, and we will use the chardet library to
discover what type of encoding it is. After which we will use the encoding 
parameter of Pandas to properly load the CSV file.''')


# In[30]:


code = '''# Import the needed library
import chardet

# Create a dict with file paths
files = {"NetflixOriginals.csv": "./data/NetflixOriginals.csv", "netflix.csv": "./data/netflix.csv", "netflix1.csv": "./data/netflix1.csv"}

# Loop through the dict, and print out the names and encoding type 
for name, file in files.items():
  with open(file, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))
  print(name, result)'''
st.code(code, language = "python")


# In[31]:


st.header('Loading in and Merging the Dataframes')


# In[32]:


st.text('''Now we can start loading the datasets into Pandas with the `read_csv` function,
and we will use the `merge` function to join the dataframes together.

- Note: It's only mandatory to use the encoding parameter for the Windows-1252 enconding, 
because Pandas doesn't have problems with loading in the other encoding formats''')


# In[33]:


code = '''# Import Pandas
import pandas as pd

# Import the first dataset, and decode the csv file with Windows-1252 encoding
df = pd.read_csv("./data/NetflixOriginals.csv", encoding="Windows-1252")

# Change the column name of Premiere and set the format in DateTime to match the other dataset 
df.rename(columns = {"Premiere": "Date"}, inplace=True)
df.rename(columns = {"Title": "title"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])

# Load in the second dataset
df2 = pd.read_csv("./data/netflix1.csv")

# Load in the third dataset
df3 = pd.read_csv("./data/netflix.csv")

df3["Date"] = pd.to_datetime(df3["Date"])'''
st.code(code, language= "python")


# In[34]:


code = '''# Create a new dataframe by merging df, df2, df3 on shared column names and using the Left Join
netflix_df = df.merge(df2[["title", "rating"]], on="title", how="left") \
        .merge(df3, on="Date", how="left") 
netflix_df.head()'''
st.code(code, language = "python")


# In[35]:


st.text('''The Rating column and all the columns with Stock data have NaN values.We now have to 
decide what we want to do with the those rows, there are two main options 
for this: `pd.fillna` or `pd.dropna`. 

Rating column
For the Rating column we have decided to fill all NaN values with U for
unknown, because 80 rows would be alot of data to discard.

Stock data columns
For the Stock data columns we've tried to apply the `pd.interpolate` 
function, but it wasn't succesfull . We've decided to drop the rows in 
question, because dropping 36 rows could be better justified''')


# In[36]:


code = '''# Sort all values in the Dataframe by date, to order the data first
netflix_df.sort_values("Date", inplace=True)

# Fill the NaN values of the rating column with U 
netflix_df["rating"].fillna("U", inplace=True)

# Drop all rows with NaN values
netflix_df.dropna(inplace=True)'''

st.code(code, language = "python")


# In[37]:


# Create a exchange rate difference column, to with the difference between the High and Low points of the day
netflix_df["Daily exchange rate difference"] = netflix_df["Open"] - netflix_df["Close"]

# Create a DataFrame with the top 20 movies with the highest IMDB Scores
imdb_top20 = netflix_df.sort_values(['IMDB Score'], ascending=False)[0:20]

# Show the first 5 rows
netflix_df.head()


# In[38]:


# Maak een streamlit dataframe zodat hij weergeven wordt op de app
st_netflix_df = st.dataframe(netflix_df)


# In[39]:


st.title('''Visualizing the data''')


# In[40]:


st.header('''Genre distribution''')


# In[41]:


st.text('''We First want to see the Genre distribution of our movie data. We're using a bar
chart to visualize the amount of movies per Genre.''')


# In[42]:


code = """import plotly.express as px
fig = px.bar(netflix_df , x='Genre', title="Movie count by Genre")
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(width=1000, height=1000)

st.plotly_chart(fig)
fig.show()"""
st.code(code, language="python")


# In[43]:


import plotly.express as px
fig = px.bar(netflix_df , x='Genre', title="Movie count by Genre")
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(width=1000, height=1000)

st.plotly_chart(fig)
fig.show()


# In[44]:


st.text('''
We notice in the visualisation that we have alot of data in three categories, and 
that the other categories have almost no data. This means that our dataset probably
would have been better with more data distribution''')


# In[45]:


st.header('''Daily Exchange rate progression over the years, and comparing it to the IMDB Scores''')


# In[46]:


st.text('''
Now we want to look what the Daily Exchange rate is over the years, we'll be using a
line diagram to visualize this. After which we want to compare the Daily Exchange 
rate to the IMDB Scores, where we'll use a scatter plot. 
 ''')


# In[47]:


code= """fig = px.line(netflix_df, 
              x="Date", 
              y="Daily exchange rate difference",
              title= "Daily Exchange Rate Difference by Year",
              labels= {"Date": "Year", "Daily exchange rate difference": "Daily Exchange Rate Difference"},
              hover_name="title")
fig.update_layout(width=1000, height=1000)
st.plotly_chart(fig)
fig.show()"""
st.code(code, language="python")


# In[48]:


fig = px.line(netflix_df, 
              x="Date", 
              y="Daily exchange rate difference",
              title= "Daily Exchange Rate Difference by Year",
              labels= {"Date": "Year", "Daily exchange rate difference": "Daily Exchange Rate Difference"},
              hover_name="title")
fig.update_layout(width=1000, height=1000)
st.plotly_chart(fig)
fig.show()


# In[ ]:





# In[51]:


code = """fig = px.scatter(netflix_df, 
                x="IMDB Score", 
                y="Daily exchange rate difference",
                color="Genre",
                title="Daily Exchange Rate Difference by IMDB Score & Genre",
                labels= {"exchange rate difference" : "Daily Exchange Rate Difference", "IMDB Score": "IMDB Score"})
fig.update_layout(width=1000, height=1000)
st.plotly_chart(fig)
fig.show()"""
st.code(code, language="python")


# In[52]:


fig = px.scatter(netflix_df, 
                x="IMDB Score", 
                y="Daily exchange rate difference",
                color="Genre",
                title="Daily Exchange Rate Difference by IMDB Score & Genre",
                labels= {"exchange rate difference" : "Daily Exchange Rate Difference", "IMDB Score": "IMDB Score"})
fig.update_layout(width=1000, height=1000)
st.plotly_chart(fig)
fig.show()


# In[53]:


st.text('''
We noticed from the last graph that the IMDB Scores have no correlation to the stock
prices of that day. The IMDB scores are accumulated over a period of time after the
release of a movie, and don't give a good overview of the sentiment up to the 
release itself.
 ''')


# In[54]:


st.header('''IMDB Scores by Genre''')


# In[55]:


st.text('''
Now we want to visualize how the top 20 IMDB scores are distributed over the Genres,
for which we make a Dataframe with the relevant data. We'll use both a pie chart and
bar graph to visualize this.
 ''')


# In[56]:


code = '''import plotly.graph_objects as go

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
fig.show()'''
st.code(code, language="python")


# In[57]:


import plotly.graph_objects as go

labels = imdb_top20["Genre"]
values = imdb_top20["IMDB Score"]
colours = px.colors.sequential.Aggrnyl

fig = go.Figure()
fig.add_trace(go.Pie(labels=labels, 
                     values=values, 
                     pull=[0.2, 0, 0.3, 0],
                     marker= {'colors' : colours}))
fig.update_layout(title="Top 20 IMDB Scores distribution by Genre",
                  width=1000, height=1000)
st.plotly_chart(fig)
fig.show()


# In[58]:


code = """fig = px.bar(imdb_top20, 
             x="IMDB Score",
             y="title",
             color="Genre",
             labels={"title": "Movie Title"},
             title="Top 20 Movies by IMDB Scores")
fig.update_layout(width=1000, height=1000)
fig.show()"""
st.code(code, language="python")


# In[59]:


fig = px.bar(imdb_top20, 
             x="IMDB Score",
             y="title",
             color="Genre",
             labels={"title": "Movie Title"},
             title="Top 20 Movies by IMDB Scores")
fig.update_layout(width=1000, height=1000)
fig.show()


# In[72]:


st.text('''
In the visualizations we see that most of the best scores are concentrated in
Documentary, which also has the most rows in the data. This probably has a 
connection with the data distribution of the dataset being to small.
 ''')


# In[61]:


st.header('''IMDB Scores by PG-Rating''')


# In[62]:


st.text('''
For our last visualisation we want to see how the IMDB Scores are distributed over
the different PG-Ratings, for which we'll use a scatter plot.
 ''')


# In[63]:


code = """rating_buttons = [{'label': "All", 'method': "update", 'args': [{"visible": [True, True, True, True, True, True, True, True, True, True]},{'title':'All'}]},
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
fig.update_layout(title="Netflix Movies' PG-rating and their IMDB score ")
st.plotly_chart(fig)
fig.show()"""
st.code(code, language="python")


# In[67]:


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
fig.update_layout(title="Netflix Movies' PG-rating and their IMDB score ")
fig.update_layout(width=1000, height=1000)
st.plotly_chart(fig)
fig.show()


# In[65]:


st.text('''
In this visualisation we can see that PG-Rating has no corralation with the IMDB 
rating, because the different rating groups are spread out around the plot.
 ''')


# In[71]:


code = '''netflix_df['quarter'] = pd.PeriodIndex(netflix_df.Date, freq='Q')

quarter_close_med = netflix_df.groupby('quarter')['Close'].median()
quarter_imdb_med = netflix_df.groupby('quarter')['IMDB Score'].median()

quarter = pd.concat([quarter_close_med, quarter_imdb_med], axis=1, join='inner')
quarter['Percentage Change'] = quarter['Close'].pct_change() * 100
quarter['Quarter'] = quarter.index.to_timestamp()

fig = px.line(data_frame=quarter, x='Quarter', y='IMDB Score', 
              labels={
                     "Quarter": "Date",
                     "IMDB Score": "Median IMDB Score",
                     "species": "Species of Iris"
                 },
                title="Median IMDB Score of Netflix Originals through the years")
st.plotly_chart(fig)
fig.show()'''
st.code(code, language='python')


# In[70]:


netflix_df['quarter'] = pd.PeriodIndex(netflix_df.Date, freq='Q')

quarter_close_med = netflix_df.groupby('quarter')['Close'].median()
quarter_imdb_med = netflix_df.groupby('quarter')['IMDB Score'].median()

quarter = pd.concat([quarter_close_med, quarter_imdb_med], axis=1, join='inner')
quarter['Percentage Change'] = quarter['Close'].pct_change() * 100
quarter['Quarter'] = quarter.index.to_timestamp()

fig = px.line(data_frame=quarter, x='Quarter', y='IMDB Score', 
              labels={
                     "Quarter": "Date",
                     "IMDB Score": "Median IMDB Score",
                     "species": "Species of Iris"
                 },
                title="Median IMDB Score of Netflix Originals through the years")
st.plotly_chart(fig)
fig.show()


# In[ ]:


st.text('''This plot shows the median of the IMDB scores each quarter. It seems like
is a downward trend of the IMDB scores of the Netflix movies.''')


# In[ ]:


st.header("Main takeaways")


# In[69]:


st.text('''
- The stock data wasen't suitable to combine with the movie data with IMDB scores 
- The data distribution of the dataset was very poor
- Having data about the amount of IMDB voters, or total Netflix subscribers could
have provided more insights
 ''')


# In[ ]:




