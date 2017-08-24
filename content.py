# linreg.py
#
# Standalone Python/Spark program to perform linear regression.
# Performs linear regression by computing the summation form of the
# closed form expression for the ordinary least squares estimate of beta.
# 
# TODO: Write this.
# 
# Takes the yx file as input, where on each line y is the first element 
# and the remaining elements constitute the x.
#
# Usage: spark-submit linreg.py <inputdatafile>
# Example usage: spark-submit linreg.py yxlin.csv
#
#

## Submitted by Sai Nikhil Gundu, Id: 800962726

#groupId = org.apache.spark
#artifactId = spark-core_2.11
#version = 2.1.0

#groupId = org.apache.hadoop
#artifactId = hadoop-client
#version = Hadoop 2.6.0-cdh5.8.0

# Code developed using the skeleton code provided as base


import sys
import numpy as np

from pyspark import SparkContext

#Set the precision value for the output. 
np.set_printoptions(precision=13)

# defining the keys for computing beta values. (using the class lecture notes)


if __name__ == "__main__":
 

  sc = SparkContext(appName="Content Based")

  # Input yx file has y_i as the first element of each line 
  # and the remaining elements constitute x_i
  ratings_raw_data = sc.textFile(sys.argv[1])
  ratings_raw_data_header = ratings_raw_data.take(1)[0]

  movies_raw_data = sc.textFile(sys.argv[2])
  movies_raw_data_header = movies_raw_data.take(1)[0]
  #yxinputFile = sc.textFile(sys.argv[1])
  #yxlines = yxinputFile.map(lambda line: line.split(','))
  
  ratings_data = ratings_raw_data.filter(lambda line: line!=ratings_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[1],tokens[2])).cache()
  ratings_1_data_forM_U = ratings_raw_data.filter(lambda line: line!=ratings_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[1],tokens[0],tokens[2])).cache()
    
  

  movies_data = movies_raw_data.filter(lambda line: line!=movies_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[1])).cache()
  
  #Calculating training and test splits-Using entire data as training
  
  training_RDD, test_RDD = ratings_data.randomSplit([10,0], seed=9)
  training_RDD1,test_RDD1 = ratings_1_data_forM_U.randomSplit([10,0], seed=9)
  
  # Creating sparse representation of A matrix with users as rows and items as columns

  user_item_ratings = (training_RDD
                          .map(lambda p: (p[0],p[-2:])).groupByKey()).cache()
  
  item_user_ratings=(training_RDD1
                          .map(lambda p: (p[0],p[-2:])).groupByKey()).cache()
    
  

  user_ratings=ratings_data.map(lambda X: (X[0], X[2]))
    
  movie=ratings_data.map(lambda x: (x[2],x[1]))

  userId = (sys.argv[3])
  
  ur_broadcast = sc.broadcast({
    k: v for (k, v) in user_ratings.collect()
  })

  u_r= np.array(user_ratings.lookup(userId))
  


  #Movie broadcast
  
  m_broadcast = sc.broadcast({
    k: v for (k, v) in movie.collect()
  })

  movies_broadcast = sc.broadcast({
    k: v for (k, v) in movies_data.collect()
  })
 
  array1 = u_r[u_r.argsort()[-5:]]
  top_movie=m_broadcast.value[array1[0]]
  #top_movie=m_broadcast.value['3.0']
  
  print top_movie
  
  g_m=movies_raw_data.filter(lambda line: line!=movies_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[0],tokens[2])).cache()
    
  m_g=movies_raw_data.filter(lambda line: line!=movies_raw_data_header)\
    .map(lambda line: line.split(",")).map(lambda tokens: (tokens[2],tokens[0])).cache()
    
  m_broadcast = sc.broadcast({
    k: v for (k,v) in g_m.collect()
  })

  top_genre=m_broadcast.value[top_movie]
    
  g_broadcast = sc.broadcast({
    v: k for (k,v) in g_m.collect()
  })

  m_r_broadcast = sc.broadcast({
    v: k for (k,v) in movie.collect()
  })
  
  lookup_content=np.array(m_g.lookup(top_genre))
    
  genre_ratings=[0.0000]*len(lookup_content)

  for i, j in zip(range(5),lookup_content):
      genre_ratings[i]=m_r_broadcast.value[j]
    
  g_r=np.array(genre_ratings)

  top_movies_genre=lookup_content[g_r.argsort()[-5:]]
   
  print "----------------------------------------------------------------------"
  print "Based on the genre, top rated movies calculation"
  print "----------------------------------------------------------------------"
  
  print "Recommended movies for userId", userId
  for i, j in zip(range(5),top_movies_genre):
      print("Movie Id=", j, " with title=", movies_broadcast.value[top_movies_genre[i]])
  

    
  


  sc.stop()
