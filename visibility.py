#!/usr/bin/python3
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

def co_refract(alt, observer_alt=0.0, pressure=None, temperature=None, \
                   epsilon=0.25, convert_to_observed=False, full_output=True):
    """
    Convert between apparent (real) altitude and observed altitude.
    Taken from PyAstronomy module
    """
    old_alt = np.array(alt, ndmin=1)
    
    if observer_alt is not None:
        # Observer altitude has been given
        obsalt = np.array(observer_alt, ndmin=1)
    else:
        # Assume that observer is  at altitude 2000m.
        obsalt = np.empty(old_alt.size)
        obsalt[:] = 2000.0

    if temperature is not None:
        # Temperature is given
        temper = np.array(temperature, ndmin=1)
        # Convert temperature to Kelvin
        temper += 273.15
    else:
        # Calculate based on observatory elevation
        alpha = 0.0065 # deg C per metre
        temper = np.zeros(old_alt.size) + 283. - alpha*obsalt
        ind = np.where(obsalt > 11000.)[0]
        if len(ind) > 0:
            temper[ind] = 211.5

    # Estimate Pressure based on altitude, 
    # using U.S. Standard Atmosphere formula.
    if pressure is not None:
        # Pressure has been specified
        pres = np.array(pressure, ndmin=1)
    else:
        # Use default atmospheric pressure
        pres = 1010.*(1.0-6.5/288000.0*obsalt)**5.255

    if not convert_to_observed:
        altout = old_alt - co_refract_forward(old_alt, pressure = pres, \
                                                  temperature = temper - 273.15)
    else:
        # Convert from real to observed altitude
        altout = np.zeros(len(old_alt))
        for i in range(len(old_alt)):
            dr = co_refract_forward(old_alt[i], pressure = pres[i], \
                                        temperature = temper[i] - 273.15)
            # Guess of observed location
            cur = old_alt[i] + dr
            while True:
                last = cur.copy()
                dr = co_refract_forward(cur, pressure = pres[i], \
                                            temperature = temper[i] - 273.15)
                cur = old_alt[i] + dr
                if np.abs(last - cur)*3600. < epsilon:
                    break
            altout[i] = cur.copy()

    if full_output:
        return altout, pres, temper
    else:
        return altout
    
def co_refract_forward(alt, pressure=1010., temperature=10.0):
    """
    Calculate the conversion between the apparent (real) RA and Dec
    and the observed RA and Dec from a telescope as a result of
    refraction through the atmosphere
    Called by co_refract
    """
  
    alt = np.array(alt, ndmin=1)
    pres = np.array(pressure, ndmin=1)
    # Temperature in Kelvin
    temper = np.array(temperature, ndmin=1) + 273.15

    # You observed the altitude alt, and would like to know what the 
    # "apparent" altitude is (the one behind the atmosphere).
    R = 0.0166667 / np.tan( (alt + 7.31/(alt+4.4))*np.pi/180. )
    w = np.where(alt < 15.)[0]
    if len(w) > 0:
        R[w] = 3.569*(0.1594 + 0.0196 * alt[w] + \
                          0.00002 * alt[w]**2)/(1. + 0.505 * alt[w] + \
                                                    0.0845 * alt[w]**2)
    tpcor = pres/1010. * 283./temper
    R *= tpcor
    return R

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

def h_to_el(h_in, dec_in, phi0_in, elev_in):
    """
    Calculate elavation coordinate, a, given hour angle (h_in),
    declination of source (dec_in) and latitude of observatory (phi0_in)

    Input angles in degrees (elev_in in metres)

    sin(a) = sin(phi0)sin(dec) + cos(phi0)cos(dec)cos(h)
    """
    phi0_rad = np.radians(phi0_in)
    dec_rad = np.radians(dec_in)
    h_rad = np.radians(h_in)
    term_1 = np.sin(phi0_rad) * np.sin(dec_rad)
    term_2 = np.cos(phi0_rad) * np.cos(dec_rad) * np.cos(h_rad)
    apparent_alt = np.degrees(np.arcsin(term_1 + term_2))
    # Correct for atmospheric refraction
    elev_arr = np.empty(len(apparent_alt))
    elev_arr.fill(elev_in)
    obs_alt = co_refract(apparent_alt, observer_alt = elev_arr, \
                             convert_to_observed = True, full_output = False)
    # Calculate the airmass from the apparent altitude
    airmass = airmass_calc(apparent_alt)
    return obs_alt, airmass

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

def sun_moon_coords(object_in, time_in):
    """
    Calculate the RA and Dec (and phase for Moon) given
    the time using the ephem package
    """
    obj_ra = np.empty(len(time_in))
    obj_dec = np.empty(len(time_in))
    if object_in == "Sun":
        obj = ephem.Sun()
        for ind in range(len(time_in)):
            obj.compute(time_in[ind])
            obj_ra[ind] = obj.g_ra * 180.0 / np.pi
            obj_dec[ind] = obj.g_dec * 180.0 / np.pi
        return obj_ra, obj_dec
    elif object_in == "Moon":
        obj = ephem.Moon()
        obj_phase = np.empty(len(time_in))
        for ind in range(len(time_in)):
            obj.compute(time_in[ind])
            obj_ra[ind] = obj.g_ra * 180.0 / np.pi
            obj_dec[ind] = obj.g_dec * 180.0 / np.pi
            obj_phase[ind] = obj.phase
        return obj_ra, obj_dec, obj_phase
    else:
        return np.array([]), np.array([])

def visibility(points, ra_in, dec_in, long_obs, lat_obs, sn_ra_in, sn_dec_in, \
                   mn_ra_in, mn_dec_in, mn_phase_in, JD_arr, elev_obs = 2830, \
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
    pd_cols = ["date_dec", "obj_ra", "obj_dec", "obj_alt", "obj_airmass", \
                   "mn_ra", "mn_dec", "mn_alt", "mn_airmass", \
                   "sn_ra", "sn_dec", "sn_alt", "sn_airmass", "mn_dist", \
                   "mn_phase", "day_night"]
    obj_df = pd.DataFrame(index = range(points), columns = pd_cols)
#    obj_df["date_dec"] = time_arr_full
    obj_df["date_dec"] = JD_arr
    obj_df.loc[:, "obj_ra"] = float(ra_in)
    obj_df.loc[:, "obj_dec"] = float(dec_in)
    # """
    obj_df.loc[:, "mn_ra"] = mn_ra_in
    obj_df.loc[:, "mn_dec"] = mn_dec_in
    obj_df.loc[:, "mn_phase"] = mn_phase_in
    obj_df.loc[:, "sn_ra"] = sn_ra_in
    obj_df.loc[:, "sn_dec"] = sn_dec_in
    # Calculate the Moon distance
    obj_df["mn_dist"] = ang_sep(obj_df["mn_ra"].astype(float),\
                                    obj_df["obj_ra"].astype(float),\
                                    obj_df["mn_dec"].astype(float),\
                                    obj_df["obj_dec"].astype(float))
    #"""
    """
    old code
    # Loop through for all times on the grid
    pre_loop_time = datetime.now()
    for ind in range(len(time_arr_full)):
        obj_df.loc[ind, "date_str"] = "%s" % \
            ephem.Date(obj_df.loc[ind, "date_dec"])
        obs.date = obj_df.loc[ind, "date_dec"]
        mn.compute(obj_df.loc[ind, "date_dec"])
        sn.compute(obj_df.loc[ind, "date_dec"])
        # Output RA and Dec seem to be in radians
        obj_df.loc[ind, "mn_ra"] = mn.a_ra * 180.0 / np.pi
        obj_df.loc[ind, "mn_dec"] = mn.a_dec * 180 / np.pi
        obj_df.loc[ind, "mn_phase"] = mn.phase
        obj_df.loc[ind, "sn_ra"] = sn.a_ra * 180.0 / np.pi
        obj_df.loc[ind, "sn_dec"] = sn.a_dec * 180.0 / np.pi

    # Calculate Moon distance
    obj_df["mn_dist"] = ang_sep(obj_df["mn_ra"].astype(float), \
                                    obj_df["obj_ra"].astype(float), \
                                    obj_df["mn_dec"].astype(float), \
                                    obj_df["obj_dec"].astype(float))
    """
    # Calculate the elevation angle of the object
    gst_arr = days_to_gst(obj_df["date_dec"])
    #"""
    obj_df["mn_alt"], obj_df["mn_airmass"]= h_to_el(gst_arr - long_obs - \
                                   obj_df["mn_ra"].astype(float), \
                                   obj_df["mn_dec"].astype(float), \
                                   lat_obs, elev_obs)
    obj_df["sn_alt"], obj_df["sn_airmass"] = h_to_el(gst_arr - long_obs - \
                                   obj_df["sn_ra"].astype(float), \
                                   obj_df["sn_dec"].astype(float), \
                                   lat_obs, elev_obs)
    #"""
    obj_df["obj_alt"], obj_df["obj_airmass"] = h_to_el(gst_arr - long_obs - \
                                                           ra_in, dec_in, \
                                                           lat_obs, elev_obs)
    """
    old code
    # Calculate the airmass of the object (Pickering, 2002)
    obj_df["obj_airmass"] = airmass_calc(obj_df["obj_alt"].astype(float))
    """
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
    plt.plot((obj_df["date_dec"] - ts0) * 24.0, obj_df["sn_alt"], \
                 color = "r", label = "Sun")
    plt.plot((obj_df["date_dec"] - ts0) * 24.0, obj_df["mn_alt"], \
                 color = "b", label = "Moon")
    plt.legend(loc = "upper right")
    plt.xlabel("Hours from now")
    plt.ylabel("Altitude angle")
    plt.savefig("observability_fig.pdf")
    #"""
    # Find where it is day, night or twilight
    night_inds = np.where(obj_df["sn_alt"] < 18.0)
    day_inds = np.where(obj_df["sn_alt"] >= 0.0)
    twilight_inds = np.where((obj_df["sn_alt"] < 0.0) & \
                              (obj_df["sn_alt"] >= 18.0))
    vis_inds = np.where((obj_df["sn_alt"] < 0.0) & \
                         (obj_df["obj_alt"] > min_elev))
    obj_df.loc[night_inds[0], "day_night"] = "night"
    obj_df.loc[day_inds[0], "day_night"] = "day"
    obj_df.loc[twilight_inds[0], "day_night"] = "twilight"
    print("Moon distance: \n", np.sum(np.isnan(obj_df["mn_dist"])))
    #"""
    # Create string for whether or not the object is observable, when and 
    # for how long
    #"""
    if len(vis_inds[0]) == 0:
        return "This event is not observable from your telescope\'s location"
    elif (obj_df.loc[0,"obj_alt"] >= 30.0) & (obj_df.loc[0, "sn_alt"] < 0.0):
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
    #"""

if __name__ == '__main__':
    start_time = datetime.utcnow()
    POINTS = 200
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

    # Create grid of times from now to 24 hours from now:
    ts0 = ephem.now()
    ts1 = ephem.date(ts0 + (24.0 * ephem.hour))
    JD_time_grid = np.linspace(ts0, ts1, POINTS)
    # Get the Sun coordinates (RA, Dec)
    sn_ra, sn_dec = sun_moon_coords("Sun", JD_time_grid)
    # Get the Moon coordinate (RA, Dec, phase)
    mn_ra, mn_dec, mn_phase = sun_moon_coords("Moon", JD_time_grid)
    """
    # Temporary Moon and Sun arrays to have to pass to visibility
    mn_ra = np.empty(len(JD_time_grid))
    mn_dec = np.empty(len(JD_time_grid))
    mn_phase = np.empty(len(JD_time_grid))
    sn_ra = np.empty(len(JD_time_grid))
    sn_dec = np.empty(len(JD_time_grid)) 
    """
    pre_vis_call = datetime.utcnow()
    print (visibility(POINTS, ra_in, dec_in, 360 - 244.5400, \
                          31.0440, sn_ra, sn_dec, mn_ra, mn_dec, \
                          mn_phase, JD_time_grid))
    post_vis1_call = datetime.utcnow()
    print (visibility(POINTS, ra_in, dec_in, 360 - 244.5400, \
                          31.0440, sn_ra, sn_dec, mn_ra, mn_dec, \
                          mn_phase, JD_time_grid))
    post_vis2_call = datetime.utcnow()
    print("Total time: " + str(post_vis2_call - start_time))
    print("Pre_vis time: " + str(pre_vis_call - start_time))
    print("vis1 time: " + str(post_vis1_call - pre_vis_call))
    print("vis2 time: " + str(post_vis2_call - post_vis1_call))
