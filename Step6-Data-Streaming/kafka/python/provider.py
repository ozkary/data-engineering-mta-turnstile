import time
import uuid
import random
from datetime import datetime

# create a Provider class

class Provider:

    def __init__(self, topic):        
        self.topic = topic

    def message(self):
        # Generate a unique message ID
        message_id = str(uuid.uuid4())

        # Get current date and time
        timestamp = datetime.now()
        current_date = timestamp.strftime('%m-%d-%y')
        current_time = timestamp.strftime('%H:%M:%S')

        # get a spark timestamp       
        format = "%Y-%m-%d %H:%M:%S"  
        ts = timestamp.strftime(format)
        
        # Generate random entries and exits between 500 and 1000
        entries = str(random.randint(500, 1000))
        exits = str(random.randint(500, 1000))

        # Generate random ac,units for the same station
        ac = 'A00' + str(random.randint(1, 2))
        unit = 'R00' + str(random.randint(1, 2))
        station = 'Test-Station'

        # Format the message in CSV format
         # Create a CSV message
        # headers = 'A/C,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS,ID,TIMESTAMP\n'
        message = f'{ac},{unit},02-00-00,{station},456NQR,BMT,{current_date},{current_time},REGULAR,{entries},{exits},{message_id},{ts}'        
        return (message_id, message)
