-------------------------------------------------
-----------------READ ME-------------------------
-------------------------------------------------

To run the ALS Spark:

Assuming the als_spark.py file (attached in the folder) in the working directory
> place the input files in the following destination 

---------------------------Execution Steps----------------------------------
------------------------------------------------------------------------------

*****STEP-I*****
Copy files to DSBA-HADOOP CLUSTER:

*Assuming the user is in the current directory where the files 'content.py', 'ratings.csv' and 'movies.csv' are located. Run the following commands

Place the files from local copy to DSBA-Hadoop:

>scp als_spark.py <username>@dsba-hadoop.uncc.edu:als_spark.py

>scp ratings.csv <username>@dsba-hadoop.uncc.edu:yr.csv

>scp movies.csv <username>@dsba-hadoop.uncc.edu:m.csv



Eg: scp als_spark.py sgundu1@dsba-hadoop.uncc.edu

* Note: Use the ninernet username and password to login to DSBA CLUSTER


*****STEP-II*****
LOGGING IN DSBA CLUSTER:

> ssh -X <username>@dsba-hadoop.uncc.edu

With the credentials, a login has to be done. Let us check the files are copied on desktop

> ls
The files should be on the display 

Copy the files to hadoop cluster, for spark submit 




*****STEP-III******


Execution:

> hadoop fs -put als_spark.py 


> hadoop fs -put r.csv


> hadoop fs -put m.csv


> spark-submit als_spark.py r.csv m.csv 20


Ths should run the spark job on MapR, displaying the recommended movies. To run the job with different python cose use
>spark-submit <pythoncode_name>.py r.csv
 m.csv 20

