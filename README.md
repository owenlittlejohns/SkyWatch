# SkyWatch

This is a quick repository showing some of the code I've been working on to provide tools to SkyWatch.

# owen_vis.py:

A code to calculate the visibility of a patch of sky to a given location on the Earth. Currently, it produce:

* A figure, which plots the height above the horizon as a function of time
* A string output stating whether the source is visible, and if so when it is next visible in hours.

Improvements planned:

* Fill the background of the plot with green for the time period when the source is 30 degrees or more above the horizon.
* Coping with the potential for more than one period of observability (an unlikely event, but may occur near the poles).
* Calculation of the Moon track.
* Calculation of the distance of the source from the Moon.

# Also for future reference:

To show some Python code, rendered correctly:

```python
import numpy as np
bob = np.array([0, 1, 2, 3])
"""
I like Python and Numpy
"""
return bob
```
