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

def RA_sexa_to_degs(RA_hrs, RA_mins, RA_secs):
    """
    Read in sexagesimal right ascension and output decimal degrees
    """
    return (RA_hrs * 15.0) + (RA_mins / 4.0) + (RA_secs / 240.0)
    
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
