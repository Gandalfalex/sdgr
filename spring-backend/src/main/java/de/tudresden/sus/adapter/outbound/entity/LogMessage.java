package de.tudresden.sus.adapter.outbound.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

import jakarta.persistence.*;
import java.time.Instant;


@Getter
@Setter
@NoArgsConstructor
@Entity(name = "LogMessage")
@Table(name = "log_messages")
@Accessors(chain = true)
public class LogMessage {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @JsonIgnore
    @Column(name = "log_id")
    private Long id;

    // I don't want a direct reference, might get quite large and slow the program down?
    @Column(name = "track_id", nullable = false)
    private Long trackId;

    @Column(name = "message")
    private String message;

    @Column(name="time_stamp")
    private Instant timeStamp;

    @Column(name = "send_session")
    private String sendSession;

    @Column(name = "data_set_name")
    private String dataSetName;
}
