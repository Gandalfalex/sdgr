package de.tudresden.dataconsumer.kafka;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;

public class ExampleKafkaListener {

    private static final Logger logger = LoggerFactory.getLogger(ExampleKafkaListener.class);

    @KafkaListener(topics = "1", groupId = "exampleGroup")
    public void listenExample(KafkaMessageHolder message) {
        logger.info("Received message: {}", message);
    }

}
