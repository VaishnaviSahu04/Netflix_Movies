import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('C:/Users/Admin/OneDrive/Desktop/Netflix_Project/movies_data.csv', lineterminator = '\n')
print(df.head())  #head shows only 5 rows by default, if we dont add head then it will show all rows
print(df.info())  #to get a quick overview of dataframe
print(df['Genre'].head())  
print(df.duplicated().sum()) # duplicate is used to check the duplicate value in the given dataset and if we dont add sum it shows false in every column 
print(df.describe())  # describe works for numerical data that it describes the statistics of the dataset, for example: count, mean, std,min, 25%, 50%, 75%, and max

'''
#Exploration Summary
- we have a dataframe consisting of 9827 rows and 9 columns
- our dataset looks a like a bit tidy with no NaNs nor duplicated values
- Release_Date column needs to be casted into data time and to extract only the year value
- Overview, Original_language and poster_Url won't be so useful during analysis, so we'll drop them
- there is no noticable outliers in popularit column
- Vote_Average better be categorised for proper analysis
- Genre column has a comma separated values and whitespaces that needs to be handles and casted into categor 
'''
# Data Preprocessing
df['Release_Date'] = pd.to_datetime(df['Release_Date'])
print(df['Release_Date'].dtypes)  # datatype of release date was object changed to integer type

df['Release_Date'] = df['Release_Date'].dt.year   # date and month is removed, we only need year
print(df['Release_Date'].dtypes)   #types of year
print(df.head())

#Dropping the columns
cols = ['Overview', 'Original_Language', 'Poster_Url']
df.drop(cols, axis=1, inplace=True)
print(df.columns)  
print(df.head(),"\n")

# Categorizing Vote_Average Column
'''
we would cut the Vote_Average values and make 4 categories: "Popular", "Average", "Below_Average" and "Not_Popular"
to describe it more using "Categorize_col()" provided above
'''
def Categorize_Cols(df, col, labels):
    edges = [df[col].describe()['min'],
             df[col].describe()['25%'],
             df[col].describe()['50%'],
             df[col].describe()['75%'],
             df[col].describe()['max']]
    df[col] = pd.cut(df[col], edges, labels = labels, duplicates='drop')
    return df

# Call the function above
labels = ['not popular', 'below average', 'average', 'popular']
Categorize_Cols(df, 'Vote_Average', labels)
df['Vote_Average'].unique()
print(df.head(), "\n")

# count of total values for each attribute
print(df['Vote_Average'].value_counts(),"\n")

# Remove not_popular movies
df.dropna(inplace= True)
print(df.isna().sum(),"\n")

# We'd split genres into lists and then explode our dataframe to have only one genre per row for each movie
df['Genre'] = df['Genre'].str.split(', ')
df = df.explode('Genre').reset_index(drop=True)
print(df.head())
#convert casting column into category
df['Genre'] = df['Genre'].astype('category')  #astype function is used to convert the datatype into column or a specified type
print(df['Genre'].cat.categories)  # cat function is used to access category-specific properties and methods when a column has a category datatype
print(df.info())
print(df.nunique())
print(df.head(),"\n")

# Data Vizualization
sns.set_style('whitegrid')
#Q1. What is the most frequent genre of movies released on netflix?
print(df['Genre'].describe())

#graph
sns.catplot(y = 'Genre', data = df, kind= 'count',
            order= df['Genre'].value_counts().index,
            color= "#428af57d")
plt.title('Genre Column Distribution')
plt.show()

#Q2 Which has highest votes in vote avg column?

df.head()
sns.catplot(y = 'Vote_Average', data= df, kind= 'count',
order= df['Vote_Average'].value_counts().index,
color= '#428af57d')
plt.title('Votes Distribution')
plt.show()

#Q3 What movie got the highest popularity? what's its genre?
print(df[df['Popularity'] == df['Popularity'].max()], "\n")

#Q4 What movie got the lowest popularity? what's its genre?
print(df[df ['Popularity'] == df['Popularity'].min()], "\n")

#Q5 Which year has the most filmmed movie?
df['Release_Date'].hist()
plt.title('Release Date Column Distribution')
plt.show()

'''
CONCLUSION

Q1: what is the most frequent genre in the dataset?
Drama genre is the most frequent genre in our dataset and has appeared more than 14% of the times among 19 other
genres

Q2: What genre has highest votes?
We have 25.5% of our dataset with popular vote(6520)rows. Drama again gets the highest popularity among fans by
being having more than 18.5% of movies popularities

Q3: What movie got the highest popularity? What's its genre?
Spider-Man: no way home has the highest popularity rate in our dataset and it has genre of action, adventure and
science giction

Q4: What movie got the lowest popularity? What's its genre?
The united states, Thread has the lowest popularity rate in our dataset and it has genre of music, drama, war, 
science-fiction and 

Q5: Which year has the most filmmed movies?
Year 2020 has the highest filming rate in our dataset

'''