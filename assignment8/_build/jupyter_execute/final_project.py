#!/usr/bin/env python
# coding: utf-8

# # Final Project: Data analysis of the Disney datasets

# # Introduction
# ## Question(s) of interests
# In this analysis, I will be investigating Disney movie Directors to determine the total gross and average gross (adjusted for inflation) of the movies they have directed. I am interested in finding out which Director(s) have the highest average gross income for the movies they directed. This is interesting because disney is no longer strictly associated to animated films, but have expended into the Marvel Universe and the Star Wars Universe. It would be interesting to know if any directors have directed films from all genre of movie as well as comparing the highest grossing directors across Disney's long history of movie making. 
# 
# ## Dataset description 
# 
# The data has been obtained from https://data.world/kgarrett/disney-character-success-00-16  (Links to an external site.) which follows https://creativecommons.org/licenses/by/4.0/ (Links to an external site.).
# 
# This database contains information on what movies has been filmed by year and the revenue of each movie made. It was originally compiled to track the movies for later analysis. 
# The Disney dataset is composed of $5$ tables, `disney_movies_total_gross.csv`, `disney_revenue_1991-2016.csv`, `disney-characters.csv`, `disney-directorss.csv`, `disney-voice-actors.csv`.  Each table is stored in a `.csv` file and contains different information about Disney movies including name, release date, genre, director, actors. I will be using the `disney_movies_total_gross.csv` and `disney_director.csv` tables formally described below:
# 
# * **disney_movies_total_gross.csv**
#     * This file contains information on Disney movies, the release date, gross revenue and gross revenue adjusted for inflation. 
# * **disney_director.csv**
#     * This file includes information on Disney movie directors; their names and the movies they directed. 

# # Methods and Results
# 
# Since I am only interested in computing the themes with the most sets, I will need to use tables that contain information on movies total gross and disney director. This implies that I will need to use the **disney_movies_total_gross** and the **disney_director** tables.
# 
# However, before moving further, let us import the tables and do some basic visualizations.

# In[1]:


# Lets import all the required libraries needed for this analysis
import altair as alt
import pandas as pd
import numpy as np
# import all the required files
total_gross = pd.read_csv("data/disney_movies_total_gross.csv")
movie_director = pd.read_csv("data/disney-director.csv")


# Lets see what the tables look like.

# In[2]:


total_gross.head()


# In[3]:


movie_director.head()


# Lets get some other information about the sets table.

# In[4]:


total_gross.info()
print(total_gross['total_gross'].dtype)


# The sets table has $579$ rows and $6$ columns. Every **movie_title** has a **release_Date**, a **total_gross**, the **inflation_adjusted_gross**. 

# Lets get some other information about the **movie_director** table.

# In[5]:


movie_director.info()


# The **movie_director** table has $56$ rows with $2$ columns. Every movie name has an **director**. 

# As a first visualization, lets look at the average inflation adjusted gross in each genre. To do this, I will merge table **movie_director** with **total_gross** as **direct_gross**. 

# In[6]:


direct_gross=total_gross.merge(movie_director, left_on='movie_title', right_on='name', how='left', indicator=True)
direct_gross


# After that I will use the **total_gross** table. I will group by director and then compute the average inflation adjusted gross for each director.

# In[7]:


#get year from releasae date, and add year column back to the dataset total_gross
# group by year and compute the average inflation adjusted gross.

#total_gross['year'] = pd.DatetimeIndex(total_gross['release_date']).year
#total_gross=total_gross.assign(year = pd.DatetimeIndex(total_gross['release_date']).year)

direct_gross['inflation_adjusted_gross'] =direct_gross['inflation_adjusted_gross'].replace({'\$': '', ',': ''}, regex=True).astype(float)
avg_inflation_gross_by_director = pd.DataFrame(direct_gross.groupby('director')['inflation_adjusted_gross'].mean().sort_values(ascending=False)).sort_values(by='director', ascending=True)
avg_inflation_gross_by_director =avg_inflation_gross_by_director.reset_index()
avg_inflation_gross_by_director.head()


# Now that we have it in the proper format, we can generate a bar plot to visualize it.

# In[8]:


# Use altair to generate a bar plot
Average_gross_plot = (
    alt.Chart(avg_inflation_gross_by_director, width=500, height=300)
    .mark_bar()
    .encode(
        x=alt.X("director:O", title="Director"),
        y=alt.Y("inflation_adjusted_gross:Q", title="Average inflation Adjusted Gross"),
    )
    .properties(title="Average of Adjusted Gross by Year")
)
Average_gross_plot


# From the above plot we can see that David Hand has the highest average gross income (adjusted for inflation).  

# As a second visualization, lets take a look at the number of movies of each director.. To do this, I need to count the movies by each director

# In[9]:


# extract rows with out NAN values in the 'parent_id' column using the drop.na() function
# themes_with_parents = themes[themes['parent_id'].notnull()]
movies_with_director = direct_gross.dropna(subset=["director"])
movies_with_director


# Now lets group by genre and count the number of movies. to do this, I will import and use the script I created with a count function that takes in a dataframe and groups it by a certian column and then applies a specified aggreating function.

# In[10]:


# import the custom script
import script as scpt

# run it on the data
movie_count = scpt.count_movie(movies_with_director, 'director','movie_title' )
movie_count


# lets do a scatter plot of the themes with the most parents.

# In[62]:


# first sort the counts and extract the top 20
top_5_movies = movie_count.sort_values(by=["count"], ascending=False)[
    :5
]

# now plot it using altair
top_5_genre_plot = (
    alt.Chart(top_5_movies, width=500, height=300)
    .mark_circle()
    .encode(
        x=alt.X("director:O", sort="y", title="Genre/Type"),
        y=alt.Y("count:Q", title="Number of Movies"),
    )
    .properties(title="Top 5 director made movies")
)
top_5_genre_plot


# It seems that the **Wolfgang Reitherman** is very productive

# Now it's time to answer the original question. Which directors have the most inflation gross of average of each movie? To do this, I will make a new dataframe by merging **avg_inflation_gross_by_director** and **movie_count**

# In[63]:


director_count_gross = avg_inflation_gross_by_director.merge(movie_count, left_on='director', right_on='director', how='left', indicator=True)
director_count_gross  =director_count_gross.assign(director_avg_gross_per_movie=director_count_gross['inflation_adjusted_gross'] *director_count_gross['count'])
director_count_gross

#director_count_gross_max = director_count_gross['director_avg_gross_per_movie'].max()
director_count_gross_max=director_count_gross.loc[director_count_gross['director_avg_gross_per_movie'] == director_count_gross['director_avg_gross_per_movie'].max()]
director_count_gross_max


# It seems that in fact it is **Davied Hand** has max average inflation gross per movie. 

# we can take a look at the chart of each director's inflation gross. 

# In[64]:


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


# # Discussions
# 
# In this work, I analyzed Disney movie directors and tried to calculate the total gross and average gross (adjusted for inflation) of the movies they had directed. What I discovered was suprising. The director with the highest gross (adjusted for inflation) was David Hand who directed Snow White and the Seven Dwarves in 1937. Snow White is the oldest movie in the Disney Database!
# 
# It is quite suprising that Director David Hand and his movie Snow White topped the list. My guess would have been something from the new generation of Star Wars or Marvel films, such as Star Wars Episode VII or The Avengers. Star Wars and Marvel are extremely popular in today's pop culture scene, while Snow White has been largely out of the public eye for decades. While these movies did very well, their combined total (~1.6 billion) doesnt even come close to the adjusted gross for Snow White, which came in at 5.2 billion.  
# 
# I guess there is just no subsitute for the classics!
# 
# One cavieat that should be pointed out is that David Hand only has one credit to his name. While most movies on the list grossed well into the multi-millions, there are a handful that grossed poorly (relatively speaking) and may have brought average calculations down. I tested this theory by taking the director with the highest number of movies creditited to his name, Wolfgang Reitherman with 9 movies, but one movie outlier with a $0 gross. As you can see from the chart above, Wolfgang came in second. I believe this accurately discribes his body of work as he has directed some of the most iconic Disney movies such as 101 Dalmations and The Jungle Book, he also has the lowest grossing movie on the list, The Many Adventrues of Winnie the Poo. Although, it appears that this movie may have never been released as the gross revenue reported is $0. This may or may not be true, but nonetheless, it would have brought Wolfgang's average calculation down. 
# 
# 

# # References
# 
# Not all the work in this notebook is original. Some parts were borrowed from online resources such as the Disney Character Success Database. I take no credit for parts that are not mine. They were soley used for illustration purposes.
# 
# ## Resources used
# * [Data Source](https://data.world/kgarrett/disney-character-success-00-16)
#     * This Disney database used in this work was curated by **Kelly Garrett**.
# * Inspiration for generating the plotting the Director Average per Movie (Adjusted for Inflation) created in Python code. 
# * The question of interest was inspired by curiosity in the subject.

# In[ ]:




