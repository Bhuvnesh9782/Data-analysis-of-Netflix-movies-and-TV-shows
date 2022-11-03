#!/usr/bin/env python
# coding: utf-8

# # Data analysis of Netflix movies and TV shows
# 
# TODO - Write some introduction about your project here: describe the dataset, where you got it from, what you're trying to do with it, and which tools & techniques you're using. You can also mention about the course [Data Analysis with Python: Zero to Pandas](zerotopandas.com), and what you've learned from it.

# ### Installing package 

# In[1]:


project_name = "zerotopandas-course-project-starter" # change this (use lowercase letters and hyphens only)


# In[2]:


get_ipython().system('pip install jovian --upgrade -q')


# In[3]:


import jovian
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib


# In[4]:


jovian.commit(project=project_name)


# ### loading the dataset

# In[6]:


netflix_titles_df = pd.read_csv('netflix_titles.csv')
netflix_titles_df.head()


# In[7]:


netflix_titles_df


# ## Data Preparation and Cleaning
# 
# 
# 
# 

# In[8]:


netflix_titles_df.info()


# In[9]:


netflix_titles_df.nunique()


# In[10]:


netflix_titles_df.isnull().values.any()


# In[11]:


netflix_titles_df.isnull().sum().sum()


# In[12]:


sns.heatmap(netflix_titles_df.isnull(), cbar=False)
plt.title('Null Values Heatmap')
plt.show()


# In[13]:


netflix_titles_df.isnull().sum()


# In[14]:


netflix_titles_df['director'].fillna('No Director', inplace=True)
netflix_titles_df['cast'].fillna('No Cast', inplace=True)
netflix_titles_df['country'].fillna('Country Unavailable', inplace=True)
netflix_titles_df.dropna(subset=['date_added','rating','duration'],inplace=True)


# In[15]:


netflix_titles_df.isnull().any()


# In[16]:


netflix_movies_df = netflix_titles_df[netflix_titles_df['type']=='Movie'].copy()
netflix_movies_df.head()


# In[17]:


netflix_shows_df = netflix_titles_df[netflix_titles_df['type']=='TV Show'].copy()
netflix_shows_df.head()


# In[18]:


netflix_movies_df.duration


# In[19]:


netflix_movies_df.duration = netflix_movies_df.duration.str.replace(' min','').astype(int)
netflix_shows_df.rename(columns={'duration':'seasons'}, inplace=True)
netflix_shows_df.replace({'seasons':{'1 Season':'1 Seasons'}}, inplace=True)
netflix_shows_df.seasons = netflix_shows_df.seasons.str.replace(' Seasons','').astype(int)


# In[20]:


import jovian


# In[21]:


jovian.commit()


# ## Exploratory Analysis and Visualization
# 
# **TODO** - write some explanation here.
# 
# 

# Let's begin by importing`matplotlib.pyplot` and `seaborn`.

# In[22]:


netflix_titles_df.head()


# **TODO** - Explore one or more columns by plotting a graph below, and add some explanation about it

# In[23]:


plt.figure(figsize=(7,5))
g = sns.countplot(x = netflix_titles_df.type, palette="pastel");
plt.title("Count of Movies and TV Shows")
plt.xlabel("Type (Movie/TV Show)")
plt.ylabel("Total Count")
plt.show()


# In[24]:


plt.figure(figsize=(12,6))
plt.title("% of Netflix Titles that are either Movies or TV Shows")
g = plt.pie(netflix_titles_df.type.value_counts(), explode=(0.025,0.025), labels=netflix_titles_df.type.value_counts().index, colors=['skyblue','navajowhite'],autopct='%1.1f%%', startangle=180);
plt.legend()
plt.show()


# **TODO** - Explore one or more columns by plotting a graph below, and add some explanation about it

# In[25]:


order =  ['G', 'TV-Y', 'TV-G', 'PG', 'TV-Y7', 'TV-Y7-FV', 'TV-PG', 'PG-13', 'TV-14', 'R', 'NC-17', 'TV-MA']
plt.figure(figsize=(15,7))
g = sns.countplot(x = netflix_titles_df.rating, hue=netflix_titles_df.type, order=order, palette="pastel");
plt.title("Ratings for Movies & TV Shows")
plt.xlabel("Rating")
plt.ylabel("Total Count")
plt.show()


# In[26]:


fig, ax = plt.subplots(1,2, figsize=(19, 5))
g1 = sns.countplot(x = netflix_movies_df.rating, order=order,palette="Set2", ax=ax[0]);
g1.set_title("Ratings for Movies")
g1.set_xlabel("Rating")
g1.set_ylabel("Total Count")
g2 = sns.countplot(x = netflix_shows_df.rating, order=order,palette="Set2", ax=ax[1]);
g2.set(yticks=np.arange(0,1600,200))
g2.set_title("Ratings for TV Shows")
g2.set_xlabel("Rating")
g2.set_ylabel("Total Count")
fig.show()


# In[27]:


netflix_titles_df['year_added'] = pd.DatetimeIndex(netflix_titles_df['date_added']).year
netflix_movies_df['year_added'] = pd.DatetimeIndex(netflix_movies_df['date_added']).year
netflix_shows_df['year_added'] = pd.DatetimeIndex(netflix_shows_df['date_added']).year
netflix_titles_df['month_added'] = pd.DatetimeIndex(netflix_titles_df['date_added']).month
netflix_movies_df['month_added'] = pd.DatetimeIndex(netflix_movies_df['date_added']).month
netflix_shows_df['month_added'] = pd.DatetimeIndex(netflix_shows_df['date_added']).month


# **TODO** - Explore one or more columns by plotting a graph below, and add some explanation about it

# In[28]:


netflix_year = netflix_titles_df['year_added'].value_counts().to_frame().reset_index().rename(columns={'index': 'year','year_added':'count'})
netflix_year


# In[29]:


month_year_df = netflix_titles_df.groupby('year_added')['month_added'].value_counts().unstack().fillna(0).T

plt.figure(figsize=(11,8))
sns.heatmap(month_year_df, linewidths=0.025, cmap="YlGnBu")
plt.title("Content Heatmap")
plt.ylabel("Month")
plt.xlabel("Year")
plt.show()


# **TODO** - Explore one or more columns by plotting a graph below, and add some explanation about it

# In[30]:


fig, ax = plt.subplots(1,2, figsize=(19, 5))
g1 = sns.histplot(x = netflix_movies_df.duration, color='skyblue',ax=ax[0], kde = True, stat = "density");
g1.set_xticks(np.arange(0,360,30))
g1.set_title("Duration Distribution for Netflix Movies")
g1.set_ylabel("% of All Netflix Movies")
g1.set_xlabel("Duration (minutes)")
g2 = sns.countplot(x = netflix_shows_df.seasons, color='skyblue',ax=ax[1]);
g2.set_title("Netflix TV Shows Seasons")
g2.set_ylabel("Count")
g2.set_xlabel("Season(s)")
fig.show()


# In[31]:


filtered_countries = netflix_titles_df.set_index('title').country.str.split(', ', expand=True).stack().reset_index(level=1, drop=True);
filtered_countries = filtered_countries[filtered_countries != 'Country Unavailable']

plt.figure(figsize=(7,9))
g = sns.countplot(y = filtered_countries, order=filtered_countries.value_counts().index[:20])
plt.title('Top 20 Countries on Netflix')
plt.xlabel('Titles')
plt.ylabel('Country')
plt.show()


# **TODO** - Explore one or more columns by plotting a graph below, and add some explanation about it

# In[32]:


filtered_genres = netflix_titles_df.set_index('title').listed_in.str.split(', ', expand=True).stack().reset_index(level=1, drop=True);

plt.figure(figsize=(7,9))
g = sns.countplot(y = filtered_genres, order=filtered_genres.value_counts().index[:20])
plt.title('Top 20 Genres on Netflix')
plt.xlabel('Titles')
plt.ylabel('Genres')
plt.show()


# In[ ]:





# Let us save and upload our work to Jovian before continuing

# In[33]:


import jovian


# In[34]:


jovian.commit()


# ## Asking and Answering Questions
# 
# TODO - write some explanation here.
# 
# 

# > Instructions (delete this cell)
# >
# > - Ask at least 5 interesting questions about your dataset
# > - Answer the questions either by computing the results using Numpy/Pandas or by plotting graphs using Matplotlib/Seaborn
# > - Create new columns, merge multiple dataset and perform grouping/aggregation wherever necessary
# > - Wherever you're using a library function from Pandas/Numpy/Matplotlib etc. explain briefly what it does
# 
# 

# #### Q1: TODO - ask a question here and answer it below

# In[35]:


filtered_directors = netflix_titles_df[netflix_titles_df.director != 'No Director'].set_index('title').director.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
sns.countplot(y = filtered_directors, order=filtered_directors.value_counts().index[:10], palette='mako')
plt.show()


# In[36]:


net = netflix_titles_df[netflix_titles_df['director'] == 'Rajiv Chilaka'].copy()
net


# In[ ]:





# #### Q2: TODO - ask a question here and answer it below

# In[37]:


filtered_cast = netflix_titles_df[netflix_titles_df.cast != 'No Cast'].set_index('title').cast.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
sns.countplot(y = filtered_cast, order=filtered_cast.value_counts().index[:10], palette='rocket')
plt.show()


# In[ ]:





# In[ ]:





# #### Q3: TODO - ask a question here and answer it below

# In[38]:


international_movies = netflix_titles_df[netflix_titles_df['listed_in'].str.contains('International Movies')]
intmov_year = international_movies['year_added'].value_counts().to_frame().reset_index().rename(columns={'index': 'year','year_added':'count'})
intmov_year = intmov_year[intmov_year.year != 2020]

international_shows = netflix_titles_df[netflix_titles_df['listed_in'].str.contains('International TV Shows')]
intshow_year = international_shows['year_added'].value_counts().to_frame().reset_index().rename(columns={'index': 'year','year_added':'count'})
intshow_year = intshow_year[intshow_year.year != 2020]

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=intmov_year, x='year', y='count')
sns.lineplot(data=intshow_year, x='year', y='count')
ax.set(xticks=np.arange(2008, 2020, 1))
plt.title("International content across all years (up to 2019)")
plt.legend(['International Movies','International TV Shows'])
plt.show()


# In[39]:


intmov_month_year_df = international_movies.groupby('year_added')['month_added'].value_counts().unstack().fillna(0).T

fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(intmov_month_year_df, linewidths=0.025, cmap="BuPu")
plt.title("International Movies Heatmap")
plt.ylabel("Month")
plt.xlabel("Year")
plt.show()


# In[40]:


intsho_month_year_df = international_shows.groupby('year_added')['month_added'].value_counts().unstack().fillna(0).T

fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(intsho_month_year_df, linewidths=0.025, cmap="BuPu")
plt.title("International TV Shows Heatmap")
plt.ylabel("Month")
plt.xlabel("Year")
plt.show()


# #### Q4: TODO - ask a question here and answer it below

# In[41]:


filtered_category = netflix_titles_df[netflix_titles_df.listed_in != 'unavailable'].set_index('title').listed_in.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
sns.countplot(y = filtered_category, order=filtered_category.value_counts().index[:10], palette='rocket')
plt.show()


# In[ ]:





# In[ ]:





# #### Q5: TODO - ask a question here and answer it below

# In[ ]:





# In[ ]:





# In[ ]:





# Let us save and upload our work to Jovian before continuing.

# In[42]:


import jovian


# In[43]:


jovian.commit()


# ## Inferences and Conclusion
# 
# **TODO** - Write some explanation here: a summary of all the inferences drawn from the analysis, and any conclusions you may have drawn by answering various questions.

# In[44]:


import jovian


# In[45]:


jovian.commit()


# ## References and Future Work
# 
# **TODO** - Write some explanation here: ideas for future projects using this dataset, and links to resources you found useful.

# > Submission Instructions (delete this cell)
# > 
# > - Upload your notebook to your Jovian.ml profile using `jovian.commit`.
# > - **Make a submission here**: https://jovian.ml/learn/data-analysis-with-python-zero-to-pandas/assignment/course-project
# > - Share your work on the forum: https://jovian.ml/forum/t/course-project-on-exploratory-data-analysis-discuss-and-share-your-work/11684
# > - Share your work on social media (Twitter, LinkedIn, Telegram etc.) and tag [@JovianML](https://twitter.com/jovianml)
# >
# > (Optional) Write a blog post
# > 
# > - A blog post is a great way to present and showcase your work.  
# > - Sign up on [Medium.com](https://medium.com) to write a blog post for your project.
# > - Copy over the explanations from your Jupyter notebook into your blog post, and [embed code cells & outputs](https://medium.com/jovianml/share-and-embed-jupyter-notebooks-online-with-jovian-ml-df709a03064e)
# > - Check out the Jovian.ml Medium publication for inspiration: https://medium.com/jovianml
# 
# 
#  

# In[46]:


import jovian


# In[47]:


jovian.commit()

