#!/usr/bin/python2
"""
  az_alt.py RA DEC
  A set of routines to convert from equatorial to horizontal coordinates
  Owen Littlejohns
"""
from datetime import datetime, timedelta
import sys
import ephem
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

def airmass_calc(elev_angle_in):
    """
    For a given elevation angle (also "altitude") calculate the airmass
    using the Pickering (2002) interpolative formula:
    """
    elev_rads = np.radians(elev_angle_in)
    deg_arg = elev_angle_in + (244.0/(165.0 + (47.0 * (elev_angle_in**1.0))))
    return 1.0 / (np.sin(np.radians(deg_arg)))

def ang_sep(ra_1, ra_2, dec_1, dec_2):
    """
    Calculate the angular separation in degrees
    cos(A) = cos(d1)cos(d2)cos(RA1 - RA2) + sin(d1)sin(d2)
    INPUTS MUST BE IN DECIMAL DEGREES
    """
    ra_1_rads = np.radians(ra_1)
    ra_2_rads = np.radians(ra_2)
    dec_1_rads = np.radians(dec_1)
    dec_2_rads = np.radians(dec_2)
    sine_dec_term = np.sin(dec_1_rads) * np.sin(dec_2_rads)
    cos_ra_diff = np.cos(ra_1_rads - ra_2_rads)
    cosine_term = cos_ra_diff * np.cos(dec_2_rads) * np.cos(dec_1_rads)
    cosA = cosine_term + sine_dec_term
    return np.degrees(np.arccos(cosA))

def h_to_el(h_in, dec_in, phi0_in):
    """
    Calculate elavation coordinate, a, given hour angle (h_in),
    declination of source (dec_in) and latitude of observatory (phi0_in)

    Input angles in degrees

    sin(a) = sin(phi0)sin(dec) + cos(phi0)cos(dec)cos(h)
    """
    phi0_rad = np.radians(phi0_in)
    dec_rad = np.radians(dec_in)
    h_rad = np.radians(h_in)
    term_1 = np.sin(phi0_rad) * np.sin(dec_rad)
    term_2 = np.cos(phi0_rad) * np.cos(dec_rad) * np.cos(h_rad)
    return np.degrees(np.arcsin(term_1 + term_2))

def days_since_j2000(year_in, month_in, day_in):
    """
    Calculate the number of days since 12:00:00, 1st Jan 2000
    Julian Day 1st Jan 2000 at 12:00 noon = JD 2451545.0
    """
    temp_year, temp_month = year_in, month_in
    if month_in < 2: temp_year, temp_month = year_in - 1.0, month_in + 12.0

    A = np.floor(temp_year / 100.0)
    B = 2 - A + np.floor(A / 4.0)
    julian_day = np.floor(365.25 * (temp_year + 4716.0)) + \
        np.floor(30.6001 * (1.0 + temp_month)) + day_in + B - 1524.50
    return julian_day - 2451545.0

def days_to_gst(days_in):
    """
    Convert the number of days (including fraction) since J2000.0 to
    GST. The modulo operator is used to get it in the range of 0 - 360
    """
    return (280.46061837 + (360.98564736629 * days_in)) % 360.0

def visibility(ut_time, ra_in, dec_in, long_obs = 360.0 - 244.5365, \
                   lat_obs = 31.0442, elev_obs = 2830., \
                   dec_lower_limit = -27.5, dec_upper_limit = 57.0, \
                   min_elev = 30.0):
    """
    Calculate visibility track for a source at RA = ra_in and dec = dec_in
    (coordinates in decimal degrees) on the specified UT date.

    Default coordinates and limits apply to 1.5m at San Pedro Martir
    Coordinates: 244.5365E, 31.0442N, 2830m above sea level
    Outputs that are useful:
    Time (decimal and string)
    Sun altitude angle (need to know when it has set, risen and hits -18degrees)
    Moon RA and Dec
    Moon altitude
    Moon phase
    Fixed body RA and Dec
    Distance between Moon and fixed body
    Put it all in a pandas table
    """
    obs = ephem.Observer()
    obs.lat = lat_obs * np.pi / 180.0
    obs.long = (360.0 - long_obs) * np.pi / 180.0
    obs.elevation = elev_obs
    sn = ephem.Sun()
    mn = ephem.Moon()
#    obj = ephem.FixedBody(ra = ra_in, dec = dec_in)
    # Create a linearly sampled grid spanning the next 24 hours
    ts0 = ephem.now()
    ts1 = ephem.date(ts0 + (24.0 * ephem.hour))
    n_samps = 50
    time_arr_full = np.linspace(ts0, ts1, n_samps)
    # Set up the pandas DataFrame
    pd_cols = ["date_dec", "date_str", "obj_ra", "obj_dec", "obj_alt", \
                   "obj_airmass", "moon_ra", "moon_dec", "moon_alt", \
                   "sun_ra", "sun_dec", "sun_alt", "moon_dist", "moon_phase", \
                   "day_night"]
    obj_df = pd.DataFrame(index = range(len(time_arr_full)), columns = pd_cols)
    obj_df["date_dec"] = time_arr_full
    obj_df.loc[:, "obj_ra"] = float(ra_in)
    obj_df.loc[:, "obj_dec"] = float(dec_in)
    # Loop through for all times on the grid
    pre_loop_time = datetime.now()
    for ind in range(len(time_arr_full)):
        obj_df.loc[ind, "date_str"] = "%s" % \
            ephem.Date(obj_df.loc[ind, "date_dec"])
        obs.date = obj_df.loc[ind, "date_dec"]
        mn.compute(obj_df.loc[ind, "date_dec"])
        sn.compute(obj_df.loc[ind, "date_dec"])
        # Output RA and Dec seem to be in radians
        obj_df.loc[ind, "moon_ra"] = mn.a_ra * 180.0 / np.pi
        obj_df.loc[ind, "moon_dec"] = mn.a_dec * 180 / np.pi
        obj_df.loc[ind, "moon_phase"] = mn.phase
        obj_df.loc[ind, "sun_ra"] = sn.a_ra * 180.0 / np.pi
        obj_df.loc[ind, "sun_dec"] = sn.a_dec * 180.0 / np.pi

    post_loop_time = datetime.now()
    loop_time = post_loop_time - pre_loop_time
    # Calculate Moon distance
    obj_df["moon_dist"] = ang_sep(obj_df["moon_ra"].astype(float), \
                                      obj_df["obj_ra"].astype(float), \
                                      obj_df["moon_dec"].astype(float), \
                                      obj_df["obj_dec"].astype(float))
    # Calculate the elevation angle of the object
    pre_non_loop = datetime.now()
    gst_arr = days_to_gst(obj_df["date_dec"])
    obj_df["moon_alt"] = h_to_el(gst_arr - long_obs - \
                                     obj_df["moon_ra"].astype(float), \
                                     obj_df["moon_dec"].astype(float), lat_obs)
    obj_df["sun_alt"] = h_to_el(gst_arr - long_obs - \
                                    obj_df["sun_ra"].astype(float), \
                                    obj_df["sun_dec"].astype(float), lat_obs)
    obj_df["obj_alt"] = h_to_el(gst_arr - long_obs - ra_in, dec_in, lat_obs)
    post_non_loop = datetime.now()
    non_loop_time = post_non_loop - pre_non_loop
    print "Loop time: ", loop_time
    print "Non loop time: ", non_loop_time
    # Calculate the airmass of the object (Pickering, 2002)
    obj_df["obj_airmass"] = airmass_calc(obj_df["obj_alt"].astype(float))
    # Plot out Moon, Sun and object tracks
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
    plt.figure(0)
    plt.figure(0)
    min_plot_time = np.amin((obj_df["date_dec"] - ts0) * 24.0)
    max_plot_time = np.amax((obj_df["date_dec"] - ts0) * 24.0)
    plt.axis([min_plot_time, max_plot_time, 0, 90])
    plt.grid(True)
    plt.plot((obj_df["date_dec"] - ts0) * 24.0, obj_df["obj_alt"], \
                 color = "k", label = "Object")
    plt.plot((obj_df["date_dec"] - ts0) * 24.0, obj_df["sun_alt"], \
                 color = "r", label = "Sun")
    plt.plot((obj_df["date_dec"] - ts0) * 24.0, obj_df["moon_alt"], \
                 color = "b", label = "Moon")
    plt.legend(loc = "upper right")
    plt.xlabel("Hours from now")
    plt.ylabel("Altitude angle")
    plt.savefig("observability_fig.pdf")
    # Find where it is day, night or twilight
    night_inds = np.where(obj_df["sun_alt"] < 18.0)
    day_inds = np.where(obj_df["sun_alt"] >= 0.0)
    twilight_inds = np.where((obj_df["sun_alt"] < 0.0) & \
                              (obj_df["sun_alt"] >= 18.0))
    vis_inds = np.where((obj_df["sun_alt"] < 0.0) & \
                         (obj_df["obj_alt"] > min_elev))
    obj_df.loc[night_inds[0], "day_night"] = "night"
    obj_df.loc[day_inds[0], "day_night"] = "day"
    obj_df.loc[twilight_inds[0], "day_night"] = "twilight"
    # Create string for whether or not the object is observable, when and 
    # for how long
    if len(vis_inds[0]) == 0:
        return "This event is not observable from your telescope\'s location"
    elif (obj_df.loc[0,"obj_alt"] >= 30.0) & (obj_df.loc[0, "sun_alt"] < 0.0):
        diff_vis = np.diff(vis_inds[0])
        gap_ind = np.where(diff_vis > 1.0)
        if len(gap_ind[0]) == 0:
            t_obs = (obj_df.loc[vis_inds[0][-1], "date_dec"].astype(float) - \
                            obj_df.loc[0, "date_dec"].astype(float)) * 24.0
        else:
            t_obs = (obj_df.loc[vis_inds[0][gap_ind[0]], \
                                    "date_dec"].astype(float) - \
                         obj_df.loc[0, "date_dec"].astype(float)) * 24.0
        time_obs_hour = int(np.floor(t_obs))
        time_obs_mins = int((t_obs % 1.0) * 60.0)
        # Make components of the observing duration string
        if time_obs_hour >= 2.0:
            ob_hr_str = " " + str(time_obs_hour) + " hours"
        elif time_obs_hour >= 1.0:
            ob_hr_str = " " + str(time_obs_hour) + " hour"
        else:
            ob_hr_str = ""
        if time_obs_mins >= 2.0:
            ob_min_str = " " + str(time_obs_mins) + " minutes."
        elif time_obs_mins >= 1.0:
            ob_min_str = " " + str(time_obs_mins) + " minute."
        else:
            ob_min_str = "."
        return "This object is immediately visible for a period of" + \
            ob_hr_str + ob_min_str   
    else:
        delay_time = (obj_df.loc[vis_inds[0][0], "date_dec"].astype(float) - \
                          obj_df.loc[0, "date_dec"].astype(float)) * 24.0
        delay_hours = int(np.floor(delay_time))
        delay_mins = int((delay_time % 1.0) * 60.0)
        diff_vis = np.diff(vis_inds[0])
        gap_ind = np.where(diff_vis > 1.0)
        if len(gap_ind[0]) == 0:
            t_obs = (obj_df.loc[vis_inds[0][-1], "date_dec"] - \
                            obj_df.loc[vis_inds[0][0], "date_dec"]) * 24.0
        else:
            t_obs = (obj_df.loc[vis_inds[0][gap_ind[0]], "date_dec"] - \
                            obj_df.loc[vis_inds[0][0], "date_dec"]) * 24.0
        obs_hours = int(np.floor(t_obs))
        obs_mins = int((t_obs % 1.0) * 60.0)
        # Make components of obs hour and minute strings
        if obs_hours >= 2.0: 
            ob_hr_str = " " + str(obs_hours) + " hours"
        elif obs_hours >= 1.0:
            ob_hr_str = " " + str(obs_hours) + " hour"
        else:
            ob_hr_str = ""
        if obs_mins >= 2.0:
            ob_min_str = " " + str(obs_mins) + " minutes."
        elif obs_mins >= 1.0:
            ob_min_str = " " + str(obs_mins) + " minute."
        else:
            ob_min_str = "."
        # Make components of delay hour and minute strings
        if delay_hours >= 2.0:
            del_hr_str = " " + str(delay_hours) + " hours"
        elif delay_hours >= 1.0:
            del_hr_str = " " + str(delay_hours) + " hour"
        else:
            del_hr_str = ""
        if delay_mins >= 2.0:
            del_min_str = " " + str(delay_mins) + " minutes "
        elif delay_mins >= 1.0:
            del_min_str = " " + str(delay_mins) + " minute "
        else:
            del_min_str = " "
        # Return the string
        return "You can start observing this event in" + del_hr_str + \
            del_min_str + "for a period of" + ob_hr_str + ob_min_str


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

    utn=datetime.utcnow()

    print (visibility(utn, ra_in, dec_in, long_obs = 360.0 - 342.1184, lat_obs = 28.7606))
