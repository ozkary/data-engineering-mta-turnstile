using System;
using System.Threading;
using Confluent.Kafka;
using Microsoft.Extensions.Configuration;

namespace DataStreaming {

    /**
     * KafkaProducer class
     * 
     * This class is responsible for generating and producing messages to the Kafka topic.
     */
    public class KafkaProducer
    {        
        private readonly string topic;
        private readonly KafkaConfigReader config;

        public KafkaProducer(string configFilePath, string topic)
        {
            this.config = new KafkaConfigReader(configFilePath);
            this.topic = topic;
        }
       
        public void ProduceMessages()
        {

            var dict = this.config.Configuration;            
            using (var producer = new ProducerBuilder<byte[], byte[]>(dict.AsEnumerable()).Build())
            {                
                while (true)
                {
                    // Generate a new message
                    var message = Provider.GenerateMessage();

                    try {
                        var key = message.Key ?? string.Empty;
                        var value = message.Value ?? string.Empty;

                        if (String.IsNullOrEmpty(key))
                        {
                            Console.WriteLine("Key is null or empty");
                            continue;
                        }

                        producer.Produce(topic, new Message<byte[], byte[]> { Key = KafkaSerializers.KeySerializer(key), Value = KafkaSerializers.ValueSerializer(value) },
                            (deliveryReport) =>
                            {
                                if (deliveryReport.Error.Code != ErrorCode.NoError) {
                                    Console.WriteLine($"Failed to deliver message: {deliveryReport.Error.Reason}");
                                }
                                else {
                                    Console.WriteLine($"Produced event to topic {topic}: key = {key} value = {value}");                                    
                                }
                            });

                        // Wait for 10 seconds before sending the next message
                        Thread.Sleep(10000);        

                    }
                    // add keyboard interrupt exception
                    catch (OperationCanceledException)
                    {
                        Console.WriteLine("Closing producer.");
                        producer.Flush(TimeSpan.FromSeconds(10));
                        producer.Dispose();
                    }
                    catch (ProduceException<string, string> e)
                    {
                        Console.WriteLine($"Delivery failed: {e.Error.Reason}");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Exception: {ex}");
                    }                            
                }
            }                    
        }
    }
}
