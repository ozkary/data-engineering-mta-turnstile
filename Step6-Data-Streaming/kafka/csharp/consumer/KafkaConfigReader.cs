using Microsoft.Extensions.Configuration;

namespace DataStreaming {
    
    /**
     * Kafka Configuration
     * 
     * This class is responsible for getting the kafka configuration.
     */
    public class KafkaConfigReader
    {        
        private IConfiguration configuration;

        public KafkaConfigReader(string configFilePath)
        {
            configuration = new ConfigurationBuilder()
                // .SetBasePath(System.IO.Directory.GetCurrentDirectory())
                .AddIniFile(configFilePath)
                .Build();
        }

        public string GetValue(string key)
        {
            return configuration[key] ?? string.Empty;
        }

        // property to return the dictionary reference
        public IConfiguration Configuration { get { return configuration; }}
    }      
}
