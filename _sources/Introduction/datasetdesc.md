## Dataset description 

```{image} ../dataset.png
:class: bg-primary mb-1
:width: 200px
:align: center
```


The data has been obtained from [data word](https://data.world/kgarrett/disney-character-success-00-16)  (Links to an external site.) which follows [creativecommonds](https://creativecommons.org/licenses/by/4.0/) (Links to an external site.).

This database contains information on what movies has been filmed by year and the revenue of each movie made. It was originally compiled to track the movies for later analysis. 
The Disney dataset is composed of $5$ tables, `disney_movies_total_gross.csv`, `disney_revenue_1991-2016.csv`, `disney-characters.csv`, `disney-directorss.csv`, `disney-voice-actors.csv`.  Each table is stored in a `.csv` file and contains different information about Disney movies including name, release date, genre, director, actors. I will be using the `disney_movies_total_gross.csv` and `disney_director.csv` tables formally described below:

* **disney_movies_total_gross.csv**
    * This file contains information on Disney movies, the release date, gross revenue and gross revenue adjusted for inflation. 
* **disney_director.csv**
    * This file includes information on Disney movie directors; their names and the movies they directed.