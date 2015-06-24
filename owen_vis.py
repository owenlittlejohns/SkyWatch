#!/usr/bin/python2
"""
  az_alt.py RA DEC
  A set of routines to convert from equatorial to horizontal coordinates
  Owen Littlejohns
"""

import sys
import ephem
from numpy import pi, linspace, where, floor, sin, cos, tan, arctan, arcsin
from numpy import amin, amax, median, argsort
import matplotlib.pyplot as plt
from matplotlib import font_manager

def h_to_el(h_in, dec_in, phi0_in):
    """
    Calculate elavation coordinate, a, given hour angle (h_in),
    declination of source (dec_in) and latitude of observatory (phi0_in)

    Input angles in degrees

    sin(a) = sin(phi0)sin(dec) + cos(phi0)cos(dec)cos(h)
    """
    d2r = pi / 180.0
    term_1 = sin(phi0_in * d2r) * sin(dec_in * d2r)
    term_2 = cos(phi0_in * d2r) * cos(dec_in * d2r) * cos(h_in * d2r)
    sin_a = term_1 + term_2
    return arcsin(sin_a) / d2r

def days_since_j2000(year_in, month_in, day_in):
    """
    Calculate the number of days since 12:00:00, 1st Jan 2000
    Julian Day 1st Jan 2000 at 12:00 noon = JD 2451545.0
    """
    temp_year, temp_month = year_in, month_in
    if month_in < 2: temp_year, temp_month = year_in - 1.0, month_in + 12.0

    A = floor(temp_year / 100.0)
    B = 2 - A + floor(A / 4.0)
    julian_day = floor(365.25 * (temp_year + 4716.0)) + \
        floor(30.6001 * (1.0 + temp_month)) + day_in + B - 1524.50
    return julian_day - 2451545.0

def days_to_gst(days_in):
    """
    Convert the number of days (including fraction) since J2000.0 to
    GST. The modulo operator is used to get it in the range of 0 - 360
    """
    return (280.46061837 + (360.98564736629 * days_in)) % 360.0

#def visibility(ut_time, ra_in, dec_in, long_obs = 360.0 - 244.5365, \
#                   lat_obs = 31.0442, elev_obs = 2830., \
#                   dec_lower_limit = -27.5, dec_upper_limit = 57):
def visibility(ut_time, ra_in, dec_in, long_obs = 360.0 - 100.0, \
                   lat_obs = -65.0, elev_obs = 0., \
                   dec_lower_limit = -90, dec_upper_limit = 90):
    """
    Calculate visibility track for a source at RA = ra_in and dec = dec_in
    (coordinates in decimal degrees) on the specified UT date.

    Default coordinates and limits apply to 1.5m at San Pedro Martir
    Coordinates: 244.5365E, 31.0442N, 2830m above sea level
    """
    obs = ephem.Observer()
    obs.lat = lat_obs * pi / 180.0
    obs.long = (360.0 - long_obs) * pi / 180.0
    obs.elevation = elev_obs
    sn = ephem.Sun()
    ts0 = ephem.now()
    ts1 = obs . next_setting(sn) - ts0
    ts2 = obs . next_rising(sn) - ts0
    if (ts1 > ts2): ts1=0.

    year_in, month_in, day_in = ut_time.year, ut_time.month, ut_time.day
    hour0 = utn.hour + (utn.minute + (utn.second + utn.microsecond / 1.e6) \
                            / 60.0) / 60.

    time_arr_hours = hour0 + linspace(ts1 * 24.0, ts2 * 24.0, 500)
    # Return when the source is next visibile
    if (dec_in < dec_upper_limit and dec_in > dec_lower_limit):
        days = days_since_j2000(year_in, month_in, day_in) + \
            time_arr_hours / 24.0
        gst_arr = days_to_gst(days)
        el_arr_degs = h_to_el(gst_arr - long_obs - ra_in, dec_in, lat_obs)
        # Plot out the visibility     
        # Set up the plot options to make a nice looking spectrum
        plt.rc("figure", figsize = [6, 6])
        plt.rc("figure", dpi = 200)
        plt.rc("text", usetex = "True")
        plt.rc("font", family = "serif")
        plt.rc("font", serif = "Times New Roman")
        plt.rc("ps", usedistiller = "xpdf")
        plt.rc("axes", linewidth = 0.5)
        plt.rc("legend", frameon = "False")
        plt.rc("patch", linewidth = 0.5)
        plt.rc("patch", facecolor = "black")
        plt.rc("patch", edgecolor = "black")
        plt.minorticks_on()
        # Start the first figure
        plt.figure(0)
        # Minimum meaningful value is 0 degrees - the horizon
        ymin_plt = 0.0
        # Maximum meaningful value is 90 degrees - zenith
        ymax_plt = 90.0
        # Set up the axis - folded on to a time
        plt.axis([amin(time_arr_hours % 24), amax(time_arr_hours % 24), \
                      ymin_plt, ymax_plt])
        plt.xlabel(r"Time (UT)")
        plt.ylabel(r"Elevation (degrees)")
        # Sort time
        full_sort_inds = argsort(time_arr_hours % 24.0)
        full_sort_time = time_arr_hours[])
        full_sort_el_degs =
        # Plot visibility track
        ra_in, dec_in
        if (dec_in < 0):
            pos_lab = "Position (J2000): {:.2f} {:.2f}".format(ra_in, dec_in)
        else:
            pos_lab = "Position (J2000): {:.2f} +{:.2f}".format(ra_in, dec_in)
        h = el_arr_degs >= 30.0
        if h.sum() > 0:
            print len(h)
            folded_time = time_arr_hours[h] % 24.0
            sorted_inds = argsort(folded_time)
            sorted_time = folded_time[sorted_inds]
            sorted_el_arr_degs = el_arr_degs[sorted_inds]
            sorted_dt = sorted_time[1:] - sorted_time[:-1]
            median_dt = median(sorted_dt)
            gap_inds = where(sorted_dt > 1.5 * median_dt)
            yfill_arr = [ymin_plt, ymax_plt, ymax_plt, ymin_plt]
            if(len(gap_inds[0]) == 0):
                xfill_arr = [sorted_time[0], sorted_time[0], sorted_time[-1], \
                                 sorted_time[-1]]
                plt.fill_between(xfill_arr, yfill_arr, \
                                     facecolor = "forestgreen", \
                                     edgecolor = "forestgreen", alpha = 0.1)
            else:
                for gap_ind in range(len(gap_inds)):
                    if gap_ind == 0:
                        xfill_arr = [folded_time[0], folded_time[0], \
                                         folded_time[gap_inds[0][gap_ind]], \
                                         folded_time[gap_inds[0][gap_ind]]]
                    elif gap_ind == len(folded_dt)-1:
                        xfill_arr = [folded_time[gap_inds[0][gap_ind]], \
                                         folded_time[gap_inds[0][gap_ind]], \
                                         folded_time[-1], folded_time[-1]]
                    else:
                        xfill_arr = [folded_time[gap_inds[0][gap_ind]], \
                                         folded_time[gap_inds[0][gap_ind]], \
                                         folded_time[gap_inds[0][gap_ind + 1]],\
                                         folded_time[gap_inds[0][gap_ind + 1]]]
                    plt.fill_between(xfill_arr, yfill_arr, \
                                         facecolor = "forestgreen", \
                                         edgecolor = "forestgreen", alpha = 0.1)
                        
        plt.grid(True)
        plt.plot(sorted_time, el_arr_degs, label = pos_lab, \
                     color = "k")
        plt.legend(loc = "upper left", fontsize = 10)
        plt.savefig("observability_fig.pdf", transparent = True)
        # Return when position is next visibility
        if (h.sum() > 0): return """visible in %.1f hours""" % (time_arr_hours[h][0] - hour0)

    return "not visible"


if __name__ == '__main__':
    """
    """
    if (len(sys.argv)<3):
        print ("Usage: az_alt.py RA DEC")
        sys.exit()

    ra_in, dec_in = float(sys.argv[1]), float(sys.argv[2])

    if (ra_in < 0.0 or ra_in > 360.0):
        print ("RA out of expected range (0.0 - 360.0)")
        sys.exit()

    if (dec_in < -90.0 or dec_in > 90.0):
        print ("DEC out of expected range (-90.0 - 90.0)")
        sys.exit()

    from datetime import datetime
    utn=datetime.utcnow()

    print (visibility(utn, ra_in, dec_in))
