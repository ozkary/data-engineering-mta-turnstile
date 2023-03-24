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

<img width="650px" src="../images/mta-discovery.png" alt="ozkary MTA discovery"/>

## Conclusions

Based on observations, the following conclusions can be made:

- Merge the DATE and TIME columns and create a date time column, CREATED
- The STATION column is a location dimension
- The CREATED column is the datetime dimension to enable the morning and afternoon timeframes
- The ENTRIES column  is the measure for entries
- The EXITS column is the measure for exits

## How to Run it!

### Requirements

- Install Python
- Install Pandas
- Install Jupyter notebook

Follow these steps to run the analysis

- Download a file to look at the data
  - This should create a gz file under the ../data folder

```
$ python3 mta_discovery.py --url http://web.mta.info/developers/data/nyct/turnstile/turnstile_230318.txt
```
Run the Jupyter notebook (dicovery.ipynb) to do some analysis on the data. 

- Load the Jupyter notebook to do analysis
  - First start the Jupyter server
  
```
$ jupyter notebook
```
  - See the URL on the console and click it to load on the browser
    - Click the discovery.ipynb file
      - Or open the file with VSCode and enter the URL when prompted from a kernel url

<img width="650px" src="../images/jupyter-mta.png" alt="ozkary MTA jupyter discovery"/>

<img  width="650px" src="../images/jupyter-browser.png" alt="ozkary MTA jupyter notebook loaded"/>


