

namespace DataStreaming {

    public class ProviderMessage {
        public string? Key { get; set; }
        public string? Value { get; set; }
    }

    public sealed class Provider {
        
        private Provider (){            
        }

        public static ProviderMessage GenerateMessage()
        {
            // Generate a unique message ID
            var messageId = Guid.NewGuid().ToString();

            // Get current date and time
            var currentDate = DateTime.Now.ToString("MM-dd-yy");
            var currentTime = DateTime.Now.ToString("HH:mm:ss");

            // Generate random entries and exits between 500 and 1000
            var random = new Random();
            var entries = random.Next(500, 1001).ToString();
            var exits = random.Next(500, 1001).ToString();

            // Format the message in CSV format
            var headers = "A/C,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS";
            var message = $"{headers}\nA002,R051,02-00-00,Test-Station,456NQR,BMT,{currentDate},{currentTime},REGULAR,{entries},{exits},{messageId}";

            var providerMessage = new ProviderMessage {
                Key = messageId,
                Value = message
            };
            return providerMessage;
        }

    }

    
}