using System;
using System.Collections.Generic;
using System.Text.Json;

namespace DataStreaming
{
    public sealed class KafkaSerializers
    {
        private KafkaSerializers()
        {
        }
        
        public static byte[] KeySerializer(string key)
        {
            return System.Text.Encoding.UTF8.GetBytes(key);
        }

        public static byte[] ValueSerializer(object value)
        {
            var serializedValue = JsonSerializer.Serialize(value);
            return System.Text.Encoding.UTF8.GetBytes(serializedValue);
        }

        public static string KeyDeserializer(byte[] key)
        {
            return System.Text.Encoding.UTF8.GetString(key);
        }

        #pragma warning disable
        public static T ValueDeserializer<T>(byte[] value)
        {
            var serializedValue = System.Text.Encoding.UTF8.GetString(value) ?? string.Empty;            
            return JsonSerializer.Deserialize<T>(serializedValue) ?? default(T);
        }
    }
}
