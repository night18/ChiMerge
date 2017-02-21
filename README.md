# ChiMerge
Implement ChiMerge [1992] via python

ChiMerge is announced by Randy Kerber in 1992. It is an algorithm that use X<sup>2</sup> statistics to discretize numeric attribution, which is a good method to reduce the afford of calculate before data mining.

ChiMerger consists 4 basic step:
 1. Sort the data in ascending order.
 2. Define initial intervals so that every value is in a separate interval.
 3. Calculate the X<sup>2</sup> of any two adjacent intervals .
 4. Find the smallest X<sup>2</sup>, and merge the intervals who own the X<sup>2</sup>
 5. Repeat 3 & 4 steps until all the X<sup>2</sup> is larger than threshold value.

The project use iris data as example, you can get the data from https://archive.ics.uci.edu/ml/machine-learning-databases/iris/
