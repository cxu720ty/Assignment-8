#!/usr/bin/env python
# coding: utf-8

# ## Results
# It seems that the **Wolfgang Reitherman** is very productive

# ![result](../result.png)

# Now it's time to answer the original question. Which directors have the most inflation gross of average of each movie? To do this, I will make a new dataframe by merging **avg_inflation_gross_by_director** and **movie_count**

# In[1]:


# Lets import all the required libraries needed for this analysis
import altair as alt
import pandas as pd
import numpy as np
# import all the required files
total_gross = pd.read_csv("data/disney_movies_total_gross.csv")
movie_director = pd.read_csv("data/disney-director.csv")
# import the custom script


# In[2]:


#get year from releasae date, and add year column back to the dataset total_gross
# group by year and compute the average inflation adjusted gross.

#total_gross['year'] = pd.DatetimeIndex(total_gross['release_date']).year
#total_gross=total_gross.assign(year = pd.DatetimeIndex(total_gross['release_date']).year)
direct_gross=total_gross.merge(movie_director, left_on='movie_title', right_on='name', how='left', indicator=True)
direct_gross['inflation_adjusted_gross'] =direct_gross['inflation_adjusted_gross'].replace({'\$': '', ',': ''}, regex=True).astype(float)
avg_inflation_gross_by_director = pd.DataFrame(direct_gross.groupby('director')['inflation_adjusted_gross'].mean().sort_values(ascending=False)).sort_values(by='director', ascending=True)
avg_inflation_gross_by_director =avg_inflation_gross_by_director.reset_index()
avg_inflation_gross_by_director.head()


# In[3]:


# import the custom script
import script as scpt


# In[4]:


movies_with_director = direct_gross.dropna(subset=["director"])
movie_count = scpt.count_movie(movies_with_director, 'director','movie_title' )

director_count_gross = avg_inflation_gross_by_director.merge(movie_count, left_on='director', right_on='director', how='left', indicator=True)
director_count_gross  =director_count_gross.assign(director_avg_gross_per_movie=director_count_gross['inflation_adjusted_gross'] *director_count_gross['count'])
director_count_gross

#director_count_gross_max = director_count_gross['director_avg_gross_per_movie'].max()
director_count_gross_max=director_count_gross.loc[director_count_gross['director_avg_gross_per_movie'] == director_count_gross['director_avg_gross_per_movie'].max()]
director_count_gross_max


# It seems that in fact it is **Davied Hand** has max average inflation gross per movie. 

# ![result](../davidhand.png)

# we can take a look at the chart of each director's inflation gross. 

# In[17]:


# Visualize the top 20 themes with the most sets using a bar plot.
director_count_gross_plot = (
    alt.Chart(director_count_gross, width=500, height=300)
    .mark_bar()
    .encode(
        x=alt.X("director:N", title="Directors", sort="-y"),
        y=alt.Y("director_avg_gross_per_movie:Q", title="Inflation per Movie"),
    )
    .properties(title="Director Average per Movie (Adjusted for Inflation)")
)
director_count_gross_plot


# In[ ]:




