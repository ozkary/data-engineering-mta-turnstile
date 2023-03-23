# Step 1 Discovery

 In the discovery process, we take a look at the data that is available for our analysis. We are using the MTA turnstiles information which is available at this location:

http://web.mta.info/developers/turnstile.html

We can download a single file to take a look at the data structure and make the following observations about the data:

## Observations

- It is available in weekly batches every Sunday
- The information is audited in blocks of fours hours apart
- The date and time field are on different columns
- The cumulative entries are on the ENTRIES field
- The cumulative exits are on the EXITS field
- This data is audited in blocks of fours hours apart

<img src="../images/mta-discovery.png" alt="ozkary MTA discovery"/>

## Conclusions

Based on observations, the following conclusions can be made:

- Merge the DATE and TIME columns and create a date time column, CREATED
- The STATION column is a location dimension
- The CREATED column is the datetime dimension to enable the morning and afternoon timeframes
- The ENTRIES column  is the measure for entries
- The EXITS column is the measure for exits
