"""
A set of functions to convert Right Ascension and declination between
decimal degrees and sexagesimal formats
Owen Littlejohns -- 8th July 2015

EXAMPLES:

RA_hours, RA_mins, RA_secs = RA_degs_to_sexa(RA_degs_in)
RA_degs = RA_sexa_to_degs(RA_hours, RA_mins, RA_secs)
Dec_idegs, Dec_mins, Dec_secs = Dec_degs_to_sexa(dec_degs)
Dec_degs = Dec_sexa_to_degs(Dec_degs_in, Dec_mins, Dec_secs)
"""

def RA_degs_to_sexa(RA_degs):
    """
    Read in a decimal degrees right ascension, output hours, minutes and seconds
    """
    RA_hrs = float(int(RA_degs / 15.0))
    RA_mins = float(int((RA_degs - (RA_hrs * 15.0)) * 4.0))
    RA_secs = (RA_degs - (RA_hrs * 15.0) - (RA_mins / 4.0)) * 240.0
    return RA_hrs, RA_mins, RA_secs

def RA_degs_to_sexa_str(RA_degs):
    """
    Read in a decimal degrees right ascension, return sexagemismal string
    """
    RA_hrs = float(int(RA_degs / 15.0))
    RA_mins = float(int((RA_degs - (RA_hrs * 15.0)) * 4.0))
    RA_secs = (RA_degs - (RA_hrs * 15.0) - (RA_mins / 4.0)) * 240.0
    if RA_hrs >= 0.0:
        RA_sign_str = "+"
    else:
        RA_sign_str = "-"
    RA_hrs_abs = np.abs(RA_hrs)
    RA_mins_abs = np.abs(RA_mins)
    RA_secs_abs = np.abs(RA_secs)
    if RA_hrs_abs < 10.0:
        RA_hrs_str = "0{:1.0f}".format(RA_hrs_abs)
    else:
        RA_hrs_str = "{:2.0f}".format(RA_hrs_abs)
    if RA_mins < 10.0:
        RA_mins_str = "0{:1.0f}".format(RA_mins_abs)
    else:
        RA_mins_str = "{:2.0f}".format(RA_mins_abs)
    if RA_secs_abs < 10.0:
        RA_secs_str = "0{:4.2f}".format(RA_secs_abs)
    else:
        RA_secs_str = "{:5.2f}".format(RA_secs_abs)
    return "-" + RA_hrs_str + ":" + RA_mins_str + ":" + RA_secs_str

def RA_sexa_to_degs(RA_hrs, RA_mins, RA_secs):
    """
    Read in sexagesimal right ascension and output decimal degrees
    """
    return (RA_hrs * 15.0) + (RA_mins / 4.0) + (RA_secs / 240.0)

def RA_sexa_str_to_degs(RA_str):
    """
    Read in sexagesimal string right ascension and output decimal degrees
    In progress
    """
    # Split the string by ":"
    # Check if the hrs are positive or negative - save RA_sign = +/- 1
    # Make everything the absolute values
    # Add the absolute values and multiply by the sign
    return (RA_sign) * ((RA_hrs * 15.0) + (RA_mins / 4.0) + (RA_secs / 240.0))
    
def Dec_degs_to_sexa(dec_degs):
    """
    Read in decimal degrees declination and output sexagesimal hours, mins, secs
    """
    dec_degs_out = float(int(dec_degs))
    if dec_degs >= 0.0:
        dec_mins = float(int((dec_degs - dec_degs_out) * 60.0))
        dec_secs = (dec_degs - dec_degs_out - (dec_mins / 60.0)) * 3600.0
    else:
        dec_mins = float(int((dec_degs - dec_degs_out) * 60.0)) * (-1.0)
        dec_secs = (dec_degs - dec_degs_out + (dec_mins / 60.0)) * (-3600.0)
    return dec_degs_out, dec_mins, dec_secs

def Dec_sexa_to_degs(dec_degs, dec_mins, dec_secs):
    """
    Read in sexagesimal declination and output degrees
    """
    if dec_degs >= 0.0:
        return dec_degs + (dec_mins / 60.0) + (dec_secs / 3600.0)
    else:
        return dec_degs - (dec_mins / 60.0) - (dec_secs / 3600.0)
