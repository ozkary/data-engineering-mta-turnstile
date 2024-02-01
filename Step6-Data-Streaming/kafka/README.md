# Kafka Data Streaming

## Run Kafka Locally

### Use Confluent Kafka

Use the Confluent Platform components directly.

- Download the Confluent Software

> Note:  Make sure to set the confluent platform directory as an environment variable

1. **Start Zookeeper:**
   ```bash
   zookeeper-server-start $CONFLUENT_HOME/etc/kafka/zookeeper.properties
   ```

2. **Start Kafka Broker:**
   ```bash
   kafka-server-start $CONFLUENT_HOME/etc/kafka/server.properties
   ```

3. **Create a Topic (Required):**
   ```bash
   kafka-topics --create --topic mta-turnstile --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

4. **Check the topics:**
   ```bash
   kafka-topics --list --bootstrap-server localhost:9092
   ```


These commands assume that your Confluent Platform installation is located at `/home/ozkary/confluent-7.3.2`. Adjust the paths accordingly.

If you want to use a `confluent` command, you might need to install Confluent CLI separately. You can download it from the Confluent Hub: https://www.confluent.io/hub/confluentinc/cli

Once installed, you should be able to use the `confluent` command:

```bash
confluent local start
confluent local stop
```

If you choose to use the Confluent CLI, make sure to follow the installation instructions provided by Confluent.

### Folder Structure

When you are using Kafka with Spark Structured Streaming locally, the following folders are created:

1. **commits:**
   - This folder stores the commit log for the streaming queries. It is responsible for keeping track of the offsets processed by Spark so that, in case of a failure or restart, it can resume from the last committed offset.

2. **offsets:**
   - This folder is used to store the current offset information for the Kafka data source. It helps Spark keep track of the position in the Kafka topic, ensuring that it processes each message exactly once.

3. **sources:**
   - The "sources" folder is related to the sources (like Kafka) that Spark is reading data from. It may contain metadata and state related to the specific source configuration.

4. **state:**
   - This folder is used to store the state of the streaming query. In the context of Spark Structured Streaming, it includes information about the stateful operations and aggregations. This helps in maintaining state across batches, particularly useful for windowed aggregations.

These folders are integral to the reliability and fault-tolerance mechanisms provided by Spark Structured Streaming. They help ensure that, in case of failures or restarts, the processing can resume from where it left off, maintaining exactly-once semantics and consistency.