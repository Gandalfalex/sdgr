package de.tudresden.sus.adapter.inbound.rest;


import de.tudresden.sus.adapter.inbound.dto.KafkaTemplateDTO;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/kafka")
@Slf4j
@RequiredArgsConstructor
public class KafkaController {

    @Value(value = "${spring.kafka.bootstrap-servers}")
    private String bootstrapAddress;

    @Value(value = "${spring.kafka.bootstrap-topic}")
    private String kafkaTopic;

    @GetMapping("{projectId}")
    public ResponseEntity<KafkaTemplateDTO> getKafkaTemplate(@PathVariable @NonNull Long projectId) {
        return new ResponseEntity<>(new KafkaTemplateDTO()
                .setBootstrapServers(bootstrapAddress)
                .setTopic(kafkaTopic)
                .setGroupId("1")
                .setTopicId(projectId), HttpStatus.OK);
    }
}
