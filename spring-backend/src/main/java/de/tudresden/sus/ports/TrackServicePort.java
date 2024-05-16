package de.tudresden.sus.ports;

import de.tudresden.sus.adapter.outbound.domain_objects.TrackDO;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.adapter.outbound.entity.Track;
import org.springframework.stereotype.Service;

import java.util.stream.Stream;
@Service
public interface TrackServicePort {

    Track getTrackForProject(Long projectId, Long trackId);
    Stream<Track> getAllTracksOfProject(Long projectId);
    Track createTrack(Track track);
    Track updateTrack(Long trackId, Track trackRequest);
    void deleteTrack(Project project, Long trackId);
    void addPlainDataSetToTrack(Track track, PlainData data);
    TrackDO prepareAllDataSets(Track track, String user);
}
