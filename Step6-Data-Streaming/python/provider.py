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
        current_date = datetime.now().strftime('%m-%d-%y')
        current_time = datetime.now().strftime('%H:%M:%S')

        # Generate random entries and exits between 500 and 1000
        entries = str(random.randint(500, 1000))
        exits = str(random.randint(500, 1000))

        # Format the message in CSV format
         # Create a CSV message
        headers = 'A/C,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS,ID'
        message = f'{headers}\nA002,R051,02-00-00,Test-Station,456NQR,BMT,{current_date},{current_time},REGULAR,{entries},{exits},{message_id}'        
        return (message_id, message)
