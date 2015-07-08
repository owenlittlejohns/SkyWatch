# SkyWatch

This is a quick repository containing some tools for visibility plots and coordinate transformations.

#
# conv_ra_dec.py

A collection of four Python routines to convert input right ascension and declination to or from decimal degrees (from or to sexagesimal). Outputs are all floating point variables.

Calling examples:

```python
import conv_ra_dec
RA_hours, RA_mins, RA_secs = conv_ra_dec.RA_degs_to_sexa(RA_degs_in)
RA_degs = conv_ra_dec.RA_sexa_to_degs(RA_hours, RA_mins, RA_secs)
Dec_idegs, Dec_mins, Dec_secs = conv_ra_dec.Dec_degs_to_sexa(dec_degs)
Dec_degs = conv_ra_dec.Dec_sexa_to_degs(Dec_degs_in, Dec_mins, Dec_secs)
```

# 
# owen_vis.py:

A code to calculate the visibility of a patch of sky to a given location on the Earth. Currently, it produce:

* A figure, which plots the height above the horizon as a function of time
* A string output stating whether the source is visible, and if so when it is next visible in hours.

Improvements planned:

* Fill the background of the plot with green for the time period when the source is 30 degrees or more above the horizon.
* Coping with the potential for more than one period of observability (an unlikely event, but may occur near the poles).
* Calculation of the Moon track.
* Calculation of the distance of the source from the Moon.


```
