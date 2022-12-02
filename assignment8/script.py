
def count_movie(data, grouping_col,count_col):
    import pandas as pd
    """
    Given a dataframe, a column , return a dataframe that has been
    grouped by the column 
    
    Parameters
    ----------
    data : pandas.core.frame.DataFrame
        The dataframe to sample from
    grouping_col : str
        The column to group the data on
    count_col : str
        After grouping, the column to applying th count to
   
        
    Returns
    -------
    pandas.core.frame.DataFrame 
        A dataframe with the group by column and the result of the count
        
    Raises
    ------
    TypeError
        If the input argument data is not of type pandas.core.frame.DataFrame
    AssertError
        If the input argument grouping_col is not in the data columns
    AssertError
        If the input argument count_col is not in the data columns
    
    Examples
    --------
    >>> count_movie(data, 'director','movie_title')
    Art Stevens	1

    """

    if not isinstance(data, pd.DataFrame): 
        raise TypeError("The data argument is not of type DataFrame")
    
    # Tests that the the grouping column is in the dataframe
    assert grouping_col in data.columns, "The grouping column does not exist in the dataframe"
    
    # Tests that the the action column is in the dataframe
    assert action_col in data.columns, "The action column does not exist in the dataframe"
    
    
    # compute the groupby object
    tot_movie = data.groupby(grouping_col)[count_col].agg(['count'])
    
    # convert to a dataframe
    tot_movie = pd.DataFrame(tot_movie)
    
    # reset the index
    tot_movie = tot_movie.reset_index()
    
    # return the result
    return(tot_movie)
    
    