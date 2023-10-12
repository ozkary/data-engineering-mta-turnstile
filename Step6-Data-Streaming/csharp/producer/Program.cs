﻿using System;

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
            Console.WriteLine("Producer is running");
            
            // Parse named arguments
            var namedArgs = ParseNamedArguments(args);
            
            // validate the arguments if not exit the app
            if (namedArgs.Length < 2) {
                Console.WriteLine("Usage: --topic mta-turnstile --config ~/.kafka/azure.properties");
            }
            
            // read the args [0] = topic, [1] = configuration file path            
            var topic = namedArgs.GetValueOrDefault("--topic", string.Empty);
            var configFilePath = namedArgs.GetValueOrDefault("--config", string.Empty);
            
            var kafkaProducer = new KafkaProducer(configFilePath, topic);
            kafkaProducer.ProduceMessages();
        }
    }
}

//  usage
//  dotnet run --topic mta-turnstile --config ~/.kafka/azure.properties
