using System;
using System.Threading;
using Confluent.Kafka;
using Microsoft.Extensions.Configuration;

namespace DataStreaming {

    /**
     * KafkaConsumer class
     * 
     * This class is responsible for consuming messages to the Kafka topic.
     */
    public class KafkaConsumer
    {        
        private readonly string topic;
        private readonly KafkaConfigReader config;

        public KafkaConsumer(string configFilePath, string topic, string groupId, string clientId)
        {
            this.topic = topic;
            this.config = new KafkaConfigReader(configFilePath);

            // add the group.id and client.id to the configuration
            this.config.Configuration["group.id"] = groupId;
            this.config.Configuration["client.id"] = clientId;
            // add the auto.offset.reset to the configuration
            this.config.Configuration["auto.offset.reset"] = "earliest";
            // add the enable.auto.commit to the configuration
            this.config.Configuration["enable.auto.commit"] = "false";
            // add the enable.partition eof to the configuration
            this.config.Configuration["enable.partition.eof"] = "true";

        }           
       
        public void ConsumeMessages()
        {
            var dict = this.config.Configuration;            

            // add a cancellation token
            CancellationTokenSource cts = new CancellationTokenSource();
            Console.CancelKeyPress += (_, e) => {
                e.Cancel = true; // prevent the process from terminating.
                cts.Cancel();
            };

            // create a consumer
            using (var consumer = new ConsumerBuilder<byte[], byte[]>(dict.AsEnumerable()).Build())
            {          
                consumer.Subscribe(topic);

                try
                {                    
                    while (!cts.IsCancellationRequested) 
                    {

                        // read the message
                        var result = consumer.Consume(TimeSpan.FromSeconds(10));

                        if (result == null)
                        {
                            Console.WriteLine("No message received within the timeout.");
                            continue;
                        }

                        var message = result.Message;
                        var key = KafkaSerializers.KeyDeserializer(message.Key);
                        var value = KafkaSerializers.ValueDeserializer<string>(message.Value);

                        if (String.IsNullOrEmpty(key))
                        {
                            Console.WriteLine("Key is null or empty");
                            continue;
                        }

                        Console.WriteLine($"Received message: {key}: {value}");

                        // Wait for 10 seconds before sending the next message
                        Thread.Sleep(5000);        

                    }
                }
                // add keyboard interrupt exception
                catch (OperationCanceledException)
                {
                    Console.WriteLine("Closing consumer.");                        
                }
                catch (ProduceException<string, string> e)
                {
                    Console.WriteLine($"Delivery failed: {e.Error.Reason}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Exception: {ex}");
                }  
                    finally
                {
                    consumer.Close();
                }                                          
            }                    
        }
    }
}
