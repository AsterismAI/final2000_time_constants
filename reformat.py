import sys
import os
from datetime import datetime

# -----------------------------------------------------------------------------------------------------
MONTHLOOKUP = dict( zip( range(1,13),
                         [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
                        )
                   )
# -----------------------------------------------------------------------------------------------------
def dayOfYear( year, month, day ):
    return datetime( year=year, month=month, day=day).timetuple().tm_yday

# load the file and read lines
with open( sys.argv[1], 'r' ) as F: timeData = F.readlines()

# filter for those lines that have all fields
timeData = list( filter( lambda X: len(X) > 154, timeData ) ) 

# number of good lines
N = len(timeData)

# initial value?
leapSeconds = 12

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
        if abs(ut1Rate) > 1000:
            # debugging??
            print( timeLine )
    # -----------------------------------------------------------------------
    
    # get the day of year
    doy     = dayOfYear(act_year, nMonth, nDay)

    # generate some output
    s_year = '{:02d}'.format( nYear )[:2]
    s_doy  = '{:03d}'.format( doy )
    s_date = '{:02d}-{}-{:02d}'.format( nDay, MONTHLOOKUP[nMonth], nYear )
    s_leap = '{:02d}'.format( leapSeconds )
    s_utc  = '{:5.4f}'.format( ut1mutc )
    s_rate = '{:5.4f}'.format( ut1Rate )
    s_polx = '{:6.5f}'.format( xPolar )
    s_poly = '{:6.5f}'.format( yPolar )

    print(f' {s_year} {s_doy} {s_date} {s_leap} {s_utc} {s_rate} {s_polx} {s_poly}')

