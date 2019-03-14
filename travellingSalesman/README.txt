This project is to compare the python library MLROSE against my own to solve the 
travelling salesman problem

To compare the same problem, I have created a program to generate a number of cities
randomly on a grid fo 10000 x 10000. 

The following command creates a dataset of 200 cities:
  ./createDataset.py 200 > data200.txt

Then, that dataset can be used with my own optimization program:
  ./tsp_mario.py  10000 <  data200.txt
  Where the 10000 represents the number of iterations to find the best solution

With the command above, I was able to find a solution with 260000 units of travelling
in 1.5 minutes

To run the program using the mlrose library, run:
  ./TSP_Fitness_Distance.py < data200.txt

With the command above, the solution was found in... over 30 minutes with about 960000
units of travelling.

Results are shown in the excel spreadsheet

