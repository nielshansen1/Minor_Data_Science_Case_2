#!/usr/bin/env python
# coding: utf-8

# ## DEZE MARK DOWN IS EEN TEST

# In[2]:


import streamlit as st
import pandas as pd
import numpy as np


# In[6]:


df_Spotify=pd.read_csv("SpotifyNL.csv")


# In[ ]:


st.title("DIT IS EEN TEST")


# In[7]:


st.dataframe(df_Spotify)


# In[ ]:




