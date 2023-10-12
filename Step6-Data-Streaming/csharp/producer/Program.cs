using System;

// add a namespace DataStreaming
namespace DataStreaming
{
    class Program
    {                
        static void Main(string[] args)
        {
            // clear the console
            Console.Clear();
            Console.WriteLine("Producer is running");
            
            // validate the arguments if not exit the app
            if (args.Length < 2) {
                Console.WriteLine("Usage --topic mta-turnstile --config ~/.kafka/azure.properties");
            }

            // read the args [0] = topic, [1] = configuration file path
            var topic = args[0];
            var configFilePath = args[1];

            var kafkaProducer = new KafkaProducer(configFilePath, topic);
            kafkaProducer.ProduceMessages();
        }
    }
}

//  usage
//  dotnet run --topic mta-turnstile --config ~/.kafka/azure.properties
