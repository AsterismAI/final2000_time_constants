# final2000_time_constants
A converter to generate time_constants (AstroStandards) format from publicly available finals2000A

Kerry N. Wood (kerry.wood@asterism.ai)

JAN 2025


**Overview** : the AstroStandards can't ingest the `finals_2000A` file that contains timing and Earth orientation
parameters (EOP).  Reformat that file into something the AstroStandards can eat.

**CREDIT** : big thanks to Dr. Christopher (Dane) Bass of the Aerospace Corporation for providing a version of this
code.  I reformatted and rewrote sections of it, but the logic is his!

## AstroStandards format

| Column | Format | Description |
| ------ | ------ | ----------- |
| 1 | Blank | Blank |
| 2-3 | I2 | Year (Broadcast Time), where:yy = 50-99 for years 1950-1999 or yy = 00-49 for years 2000-2049 |
| 6-8 | I3 | Day of Year (Broadcast Time) | 
| 22-24 | D3.0 | TAI-UTC (seconds) |
| 27-34 | D8.0 | UT1-UTC (seconds) |
| 37-42 | F6.0 | UT1-UTC rate (m-sec/day) |
| 46-52 | D7.0 | Polar motion X (arc-sec)  |
| 56-62 | D7.0 | Polar motion Y (arc-sec)  |
| 79-80 | A2 |Anything EXCEPT "TP" or "ZP" |
