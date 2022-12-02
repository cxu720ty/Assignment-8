#!/usr/bin/env python
# coding: utf-8

# ## Methods
# Since I am only interested in computing the themes with the most sets, I will need to use tables that contain information on movies total gross and disney director. This implies that I will need to use the **disney_movies_total_gross** and the **disney_director** tables.
# 
# However, before moving further, let us import the tables and do some basic visualizations.

# ![method](../method.png)

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


# # Lets find the way to calculate the Gross: Average and Total
# ![dollar.png](attachment:c506ed3d-91a8-4999-acde-4d39c6a2af67.png)![method](../dollar.png)

# ### Total Gross Math Equation 
# 
# \begin{alignedat}{2}y&\,=\,&x_1+x_2+\cdot\cdot\cdot+x_n\end{alignedat}

# ### Average Gross Math Equation 
# $$
# \begin{aligned}
# \bar{y}&=\frac{1}{n} \left(\sum_{i=1}^n x_i \right) 
# \end{aligned}
# $$
# 

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
