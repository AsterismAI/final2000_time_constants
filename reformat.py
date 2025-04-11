import os
from datetime import datetime

# -----------------------------------------------------------------------------------------------------
MONTHLOOKUP = dict( zip( range(1,13),
                         [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
                        )
                   )
# -----------------------------------------------------------------------------------------------------
def dayOfYear( year : int, month : int , day : int ):
    return datetime( year=year, month=month, day=day).timetuple().tm_yday

# -----------------------------------------------------------------------------------------------------
def reformatLines( timeData : list[str] ):

    '''
    Example input lines :
    73 1 2 41684.00 I  0.120733 0.009786  0.136966 0.015902  I 0.8084178 0.0002710  0.0000 0.1916  P    -0.766    0.199    -0.720    0.300   .143000   .137000   .8075000   -18.637    -3.667  
    73 1 3 41685.00 I  0.118980 0.011039  0.135656 0.013616  I 0.8056163 0.0002710  3.5563 0.1916  P    -0.751    0.199    -0.701    0.300   .141000   .134000   .8044000   -18.636    -3.571  
    73 1 4 41686.00 I  0.117227 0.011039  0.134348 0.013616  I 0.8027895 0.0002710  2.6599 0.1916  P    -0.738    0.199    -0.662    0.300   .139000   .131000   .8012000   -18.669    -3.621  
    73 1 5 41687.00 I  0.115473 0.009743  0.133044 0.013089  I 0.7998729 0.0002710  3.0344 0.1916  P    -0.732    0.199    -0.640    0.300   .137000   .128000   .7981000   -18.751    -3.769  
    73 1 6 41688.00 I  0.113717 0.011236  0.131746 0.009898  I 0.7968144 0.0002710  3.1276 0.1916  P    -0.739    0.199    -0.644    0.300   .136000   .126000   .7949000   -18.868    -3.868  
    '''
    # filter for those lines that have all fields
    timeData = list( filter( lambda X: len(X) > 154, timeData ) ) 
    # number of good lines
    N = len(timeData)

    # initial value?
    # KNW: this needs to be bolted to a known value (for now, we know 1972 is 12)
    leapSeconds = 12

    reformatted = []
    for i in range(0, N):
        timeLine = timeData[i]
        
        # two digit year
        nYear   = int(   timeLine[0:2]  )
        nMonth  = int(   timeLine[2:4]  )
        nDay    = int(   timeLine[4:6]  )
        fracjd  = float( timeLine[7:15] )

        # get the actual year
        if fracjd <= 51543: act_year = nYear + 1900
        if fracjd <= 51544: act_year = nYear + 2000

        try: ut1mutc = float(timeLine[154:165])
        except: continue
        #ut1Rate = float(timeLine[20:32])
        
        # get the polar wander values
        xPolar = float(timeLine[134:144])
        yPolar = float(timeLine[144:154])
        
        # -----------------------------------------------------------------------
        # try to infer the ut1 rate 
        nextLine = timeData[ i+1 ]
        try: ut1Next = float( nextLine[154:165] )
        #except: ut1Next = ut1mutc
        except: continue
        ut1Rate = (ut1Next - ut1mutc) * 1000
        
        if abs(ut1Rate) > 900:
            leapSeconds += 1
            # account for leap second 
            ut1Rate -= 1000
        # -----------------------------------------------------------------------
        
        # get the day of year
        doy     = dayOfYear(act_year, nMonth, nDay)

        # generate some output
        s_year = '{:02d}'.format( nYear )[:2]
        s_doy  = '{:03d}'.format( doy )
        s_date = '{:02d}-{}-{:02d}'.format( nDay, MONTHLOOKUP[nMonth], nYear )
        s_leap = '{:02d}'.format( leapSeconds )
        s_utc  = '{:+6.5f}'.format( ut1mutc )
        s_rate = '{:+4.3f}'.format( ut1Rate )
        s_polx = '{:+5.4f}'.format( xPolar )
        s_poly = '{:+5.4f}'.format( yPolar )

        # fixed width hacking
        ol        = list(' '*80)
        ol[1:2]   = s_year
        ol[5:8]   = s_doy 
        ol[11:20] = s_date
        ol[22:24] = s_leap
        ol[26:34] = s_utc
        ol[36:42] = s_rate
        ol[45:52] = s_polx
        ol[55:62] = s_poly
        ol = ''.join(ol)
        reformatted.append( ol )

    return reformatted


# =====================================================================================================
if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2 or not os.path.isfile( sys.argv[1] ):
        print('{} <finals2000 file>'.format( sys.argv[0] ) )
        sys.exit(1)

    try:
        with open( sys.argv[1], 'r' ) as F: timeLines = F.readlines()
    except Exception as e:
        print('ERROR : {}'.format( e ) )
        sys.exit(2)


    lines = reformatLines( timeLines )
    print( '\n'.join( lines ) )

