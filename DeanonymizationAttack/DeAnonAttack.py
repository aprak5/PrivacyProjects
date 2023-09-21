"""
File DeAnonAttack.py
Author: Amit Prakash (aprakas5) and Anupam Das (adas8)
Purpose: This file works with some data from a Netflix database and with some auxiliary data from IMDB.
This file works to simulate a deanonymization attack to find who the auxliary data belongs to. 
This is accomplished by finding the number of times a user rated a movie and computing a corresponding similarity score for each user.
The user with the highest similarity score is the best fit for the auxiliary data provided.
"""

#### Import all necessary modules/libraries
import re
import math
import pandas as pd
import operator

#### BEGIN----- functions to read movie files and create db ----- ####

### Add ratings to db from chunks and num as the keys/values
def add_ratings(db, chunks, num):
    '''
    Parameters
    ----------
    db : dict
        A dictionary of all users and their movies/ratings.
    chunks : dict
        Chunks parsed from the file with the user, a movie, and a rating
    num : int
        The user to parse.
        
    Returns
    -------
    None.
    '''
    if not chunks[0] in db:
        db[chunks[0]] = {}
    db[chunks[0]][num] = int(chunks[2])

### Read and parse the files provided and use add_ratings to populate db from the files
def read_files(db, num):
    '''
    Parameters
    ----------
    db : dict
        A dictionary of all users and their movies/ratings.
    num : int
        The user to parse.
        
    Returns
    -------
    None.
    '''
    movie_file = "movies/"+num
    fo = open(movie_file, "r")
    for line in fo:
        chunks = re.split(",", line)
        chunks[len(chunks)-1] = chunks[len(chunks)-1].strip()
        add_ratings(db, chunks, num)

#### END----- functions to read movie files and create db ----- ####

### Compute the similarity score using the weights, 
### maximum possible difference in ratings, and records of the user as compared to the auxiliary information. 
def score(w, p, aux, r):
    '''
    Parameters
    ----------
    w : dict
        A dictionary with the weights of movies.
    p : dict
        A dictionary with the maximum possible differences in ratings.
    aux : dict
        A dictionary with the auxiliary information.
    r : dict
        A dictionary with the records of the user/movies/ratings.

    Returns
    -------
    score : int
        The similarity score for the user as compared to the auxiliary information.
    '''
    score = 0
    for movie in r.keys(): # for each movie in the user's record
        try:
            score += (1/len(aux)) * w[movie] * (1 - ((aux[movie] - r[movie])/p[movie])) 
        except:
            score += 0 # if the movie is not found, catch the key error and add 0
    return score # return the final similarity score


### Compute the weights of movies for the database of users/movies/ratings based on the frequency of ratings.
def compute_weights(db):
    '''
    Parameters
    ----------
    db : dict
        A dictionary of all users and their movies/ratings.

    Returns
    -------
    weightMovies : dict
        A dictionary with the weights of movies.
    '''
    #### ----- your code here ----- ####
    weightMovies = {}
    ## you can use 10 base log
    for i, j in db.items(): # for each key-value pair in db
        for k, v in j.items(): # for each key-value pair in the movie-rating pair in db
            if k not in weightMovies: # if the movie is not present
                weightMovies[k] = 0 # add it with a weight of 0
            else:
                weightMovies[k] += 1 # otherwise, increment the weight by one
     ## apply the rest of the formula given in Q1a           
    for key in weightMovies.keys():
        weightMovies[key] = 1/(math.log(10, weightMovies[key]))
    return weightMovies # return the final dict of weights



#### BEGIN----- additional functions ----- ####
### Compute the maximum possible difference of movies for the database
### of users/movies/ratings based on the ratings in the database and auxiliary information.
def compute_max_diff(db, aux):
    '''
    Parameters
    ----------
    db : dict
        A dictionary of all users and their movies/ratings.
    aux : dict
        A dictionary with the auxiliary information.

    Returns
    -------
    diffMovies : dict
        A dictionary with the maximum possible differences in ratings.
    '''
    ## Define dicts for the max, min, and diff in rating for the movies
    maxMovies = {}
    minMovies = {}
    diffMovies = {}
    
    ## Use a for loop for look at each movie-rating pair and find the min and max values for each movie's ratings in the database
    for i, j in db.items():
        for k, v in j.items():
            if k not in maxMovies:
                maxMovies[k] = -1 # lower than the end of the scale
                if k not in minMovies: 
                    minMovies[k] = 6 # higher than the end of the scale
            else:
                maxMovies[k] = max(maxMovies[k], v) # save the max rating in for the max value for that movie's rating
                minMovies[k] = min(minMovies[k], v)  # save the min rating in for the max value for that movie's rating
                
    ## Use a for loop for look at each movie-rating pair and find the min and max values for each movie's ratings in the auxiliary information            
    for k, v in aux.items():
            if k not in maxMovies:
                maxMovies[k] = -1 # lower than the end of the scale
                if k not in minMovies: 
                    minMovies[k] = 6 # higher than the end of the scale
            else:
                maxMovies[k] = max(maxMovies[k], v) # save the max rating in for the max value for that movie's rating
                minMovies[k] = min(minMovies[k], v)  # save the min rating in for the max value for that movie's rating                      
    for key in maxMovies.keys():
        diffMovies[key] = maxMovies[key] - minMovies[key] # save the difference between the max and min value as the difference in rating for the movie       
    return diffMovies # return the final differences in ratings for the movies

### Compute the records of movies for the database given a user.
def compute_ratings_by_user(db, user):
    '''
    Parameters
    ----------
     db : dict
        A dictionary of all users and their movies/ratings.
    user : str
        A string describing the user.

    Returns
    -------
    r : dict
        A dictionary with the records of the user/movies/ratings.
    '''
    ## Define the dict to put records in
    r = {}
    ## Find all records of the movie-rating pairs for the user and save in r
    for i, j in db.items():
        for k, v in j.items():
            if i == user:
                r[k] = v
    return r # return the final dict of records for the user           
                
            

#### END----- additional functions ----- ####

#### Main program functionality when the file runs, handles some I/O and tabular conversion. Also, computes the similarity score for each user.
if __name__ == "__main__":
    ### Define the database of users and movie-rating pairs
    db = {}
    
    ### Populate the database of users and movie-rating pairs
    files = ["03124", "06315", "07242", "16944", "17113",
            "10935", "11977", "03276", "14199", "08191",
            "06004", "01292", "15267", "03768", "02137"]

    for file in files:
        read_files(db, file)

    ### Define and populate the auxiliary data
    aux = { '03124': 4, '06315': 3.2, '07242': 3.9, '17113': 3.7, 
            '10935': 4, '11977': 4.2, '03276': 3.8, '14199': 3.9, 
            '08191': 3.8, '03768': 2.2, '02137': 3}

    #### ----- your code here ----- #### 
    ### Define and populate the weights for the movies. Convert to a dataframe and then print out as a table. 
    w = compute_weights(db)
    ## for table formatting
    headers = ['weights'] 
    dfWeights = pd.DataFrame(w, headers).T
    dfWeights.columns.name = 'movies'
    print(dfWeights)
    print() # print a new line
    
    ### Define and populate the maximum range of ratings for the users/movies.  
    p = compute_max_diff(db, aux)
    
    ### Define and populate the similarity score dict for each user. Note this takes around 10 minutes to run.
    result = {}
    for user in db.keys():
        result[user] = score(w, p, aux, compute_ratings_by_user(db, user))
        
    ### Define and populate the topFive results from the similarity score results dict. 
    ### Convert to a dataframe and print it out in tabular form.    
    headers = ['scores'] # for table formatting
    topFive = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True)[:5]) ## sort the results array
    ## for table formatting
    dfTopFive = pd.DataFrame(topFive, headers).T 
    dfTopFive.columns.name = 'users'
    print(dfTopFive)
    print() # print a new line
    
    # 5 top values sorted by score
    ### Convert the top five users to dataframes (individually) and print them out side-by-side next to the auxiliary information.
    ## for table formatting
    headers = ['ratings']
    dfAux = pd.DataFrame(aux, headers).T
    dfAux.columns.name = 'movies'
    dfFirst = pd.DataFrame(db['716173'], headers).T
    dfFirst.columns.name = 'movies'
    dfSecond = pd.DataFrame(db['2118461'], headers).T
    dfSecond.columns.name = 'movies'
    dfThird = pd.DataFrame(db['1664010'], headers).T
    dfThird.columns.name = 'movies'
    dfFourth = pd.DataFrame(db['49890'], headers).T
    dfFourth.columns.name = 'movies'
    dfFifth = pd.DataFrame(db['2238060'], headers).T
    dfFifth.columns.name = 'movies'
    print(dfAux)
    print() # print a new line
    print(dfFirst)
    print() # print a new line
    print(dfSecond)
    print() # print a new line
    print(dfThird)
    print() # print a new line
    print(dfFourth)
    print() # print a new line
    print(dfFifth)
    print(str(topFive['716173'] - topFive['2118461'])) # difference for Q1d
    sum = 0
    for weight in w.values():
        sum += weight
    print(str((sum/len(aux))  * 0.1)) # decision for Q1d(1) (gamma = 0.1, output = gamma * m)
    print(str((sum/len(aux))  * 0.05)) # decision for Q1d(2) (gamma = 0.05, output = gamma * m)
        
    
