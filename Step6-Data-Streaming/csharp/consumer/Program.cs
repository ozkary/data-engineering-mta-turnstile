using System;

// add a namespace DataStreaming
namespace DataStreaming
{     
    class Program
    {                
        /***
        * Command line argument parser
        * 
        * Parse the command line arguments and return a dictionary of named arguments.
        */
        static Dictionary<string, string> ParseNamedArguments(string[] args)
        {
            var namedArgs = new Dictionary<string, string>();

            for (int i = 0; i < args.Length; i++)
            {
                if (args[i].StartsWith("--") && i + 1 < args.Length)
                {
                    namedArgs[args[i]] = args[i + 1];
                    i++; // Skip the next argument (the value)
                }
            }

            return namedArgs;
        }

        static void Main(string[] args)
        {
            // clear the console
            Console.Clear();
            Console.WriteLine("Consumer is running");

             // Parse named arguments
            var namedArgs = ParseNamedArguments(args);
            
            // validate the arguments if not exit the app
            if (namedArgs.Length < 4) {
                Console.WriteLine("Usage: --topic mta-turnstile --groupid turnstile --clientid appTurnstile --config ~/.kafka/azure.properties");
            }
            
            var topic = namedArgs.GetValueOrDefault("--topic", string.Empty);
            var groupId = namedArgs.GetValueOrDefault("--groupid", string.Empty);
            var clientId = namedArgs.GetValueOrDefault("--clientid", string.Empty);
            var configFilePath = namedArgs.GetValueOrDefault("--config", string.Empty);            

            var kafkaConsumer = new KafkaConsumer(configFilePath, topic, groupId, clientId);
            kafkaConsumer.ConsumeMessages();
        }
    }
}

//  usage
//  dotnet run --topic mta-turnstile --groupid turnstile --clientid appTurnstile --config ~/.kafka/azure.properties
