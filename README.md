# Urban-Planning
Part 2.  Urban planning
The problem
For this problem, you will use hill climbing and genetic algorithms to determine the ideal location of industry, commerce, and residential zones in a city.  You will input a map with the following symbols:
X:  former toxic waste site.  Industrial zones within 2 tiles take a penalty of -10.  Commercial and residential zones within 2 tiles take a penalty of -20.  You cannot build directly on a toxic waste site.
S:  scenic view.  Residential zones within 2 tiles gain a bonus of 10 points.  If you wish, you can build on a scenic site but it destroys the view.  Building on a scenic view has a cost of 1.
1...9:  how difficult it is to build on that square.  To build a zone on any square costs 2+difficulty.  So building a Commercial zone on a square of difficulty 6 costs 8 points.  You will receive a penalty of that many points to put any zone on that square.  

You will have to place industrial, residential, and commercial tiles on the terrain.  
Industrial tiles benefit from being near other industry.  For each industrial tile within 2 squares, there is a bonus of 2 points.
Commercial sites benefit from being near residential tiles.  For each residential tile within 3 squares, there is a bonus of 4 points.  However, commercial sites do not like competition.  For each commercial site with 2 squares, there is a penalty of 4 points.
Residential sites do not like being near industrial sites.  For each industrial site within 3 squares there is a penalty of 5 points.  However, for each commercial site with 3 squares there is a bonus of 4 points.

Note that all distances use the Manhattan distance approach.  So distance is computed in terms of moves left/right and up/down, not diagonal movement.
Approaches
For this component you will use:
Hill climbing with restarts and simulated annealing
Genetic algorithms 

When your hill climbing restarts, it may not modify the terrain on the map!  It can only change where it initially places the different zones (and how many zones to place) to begin the hill climbing process.  

Your hill climbing will have to trade off the number of restarts (more is better, but takes time) vs. how quickly to decrease the temperature (slower is better, but takes time).  You should also think about what actions you will allow.  Moving a zone is a sensible action.  Should there also be an action for adding/removing a zone? 

Your genetic algorithm will have to come up with a representation, selection and crossover methods, and must make use of culling, elitism, and mutation.  If you set a parameter to 0 (for example, the mutation rate), that is acceptable, but you must provide data for why you did that.  
Program behavior
Your program should accept command line input (unless difficult in your language) where the parameters are the file to read in, and the technique to use.  For example “plan map.txt GA” would read in map.txt and use the genetic algorithm approach.  “plan map.txt HC” would use hill climbing search.

Your program will read in a file where the first 3 lines are the maximum number of industrial, commercial, and residential locations (respectively).  The remainder of the file is a rectangular map of the terrain to place the town.  Your program should then run for approximately 10 seconds and output the following to a file:
The score for this map
At what time that score was first achieved.
The map, with the various industrial, commercial, and residential sites marked.  
Writeup
You should analyze your program’s behavior to answer the following questions:
Explain how you traded off number of restarts and the schedule for decreasing temperature.  We are not expecting a dissertation-level analysis, but you should provide a couple of experiments explaining how you selected your parameters.  Running a few trials works much (!) better than just making the numbers up.
Explain how your genetic algorithm works.  You must describe your selection, crossover, elitism, culling, and mutation approaches.  Give some data to explain why you selected the values that you did.  How do elitism and culling affect performance?  
Create a graph of program performance vs. time.  Run your program 10 times and plot how well hill climbing and genetic algorithms perform after 0.1, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9 and 10 seconds.  If you only had 0.25 seconds to make a decision, which technique would you use?  Does your answer change if you have 10 seconds? 
How did you perform selection and crossover for your population?  Find some known method for doing selection, other than the one described in the slides.  Explain what you did.  
