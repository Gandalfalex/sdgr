package de.tudresden.sus.service;

import de.tudresden.sus.adapter.outbound.domain_objects.DataSetDO;
import de.tudresden.sus.adapter.outbound.domain_objects.TrackDO;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.adapter.outbound.entity.Track;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.Operation;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper.SleepDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSADataSet;
import de.tudresden.sus.adapter.outbound.repositories.LogMessageRepository;
import de.tudresden.sus.adapter.outbound.repositories.ProjectRepository;
import de.tudresden.sus.adapter.outbound.repositories.TrackRepository;
import de.tudresden.sus.adapter.outbound.restclient.models.dto.TrainDataConfigurationDTO;
import de.tudresden.sus.ports.TrackServicePort;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

@Service
@Slf4j
@RequiredArgsConstructor
public class TrackService implements TrackServicePort {

    private final TrackRepository trackRepository;

    private final ProjectRepository projectRepository;

    private final LogMessageRepository logMessageRepository;

    private final DjangoRestService restService;

    /**
     * Returns the track object for the given id in the given project.
     *
     * @param projectId the given project
     * @param trackId   the track id
     * @return the track object
     */
    public Track getTrackForProject(Long projectId, Long trackId) {
        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new EntityNotFoundException("Project not found"));
        return project.getTracks().stream()
                .filter(track -> track.getId().equals(trackId))
                .findFirst()
                .orElseThrow(() -> new EntityNotFoundException("Track not found in the specified project"));
    }

    public Stream<Track> getAllTracksOfProject(Long projectId) {
        try {
            return projectRepository.findById(projectId)
                    .orElseThrow(() -> new EntityNotFoundException("Project not found")).getTracks().stream();
        } catch (EntityNotFoundException e) {
            log.error("Entity not found for ID {}: {}", projectId, e.getMessage());
            throw e;
        }
    }

    /**
     * Creates a track in the database.
     *
     * @param track the track to persist
     * @return the persisted track
     */
    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public Track createTrack(Track track) {
        track = trackRepository.save(track);
        log.info("saved track: {}", track);
        return track;
    }

    /**
     * Updates a track in the database.
     *
     * @param trackId      the id of the track to update
     * @param trackRequest the new track data
     * @return the updated track
     */
    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public Track updateTrack(Long trackId, Track trackRequest) {
        try {
            var track = trackRepository.findById(trackId).orElseThrow(() -> new EntityNotFoundException("No track found for given id"));
            track.setAllowedDataTypes(trackRequest.getAllowedDataTypes());
            track.setName(trackRequest.getName());
            track.setRepeating(trackRequest.isRepeating());
            track.setUnit(trackRequest.getUnit());
            return trackRepository.save(track);
        } catch (EntityNotFoundException e) {
            log.error("Entity not found for ID {}: {}", trackId, e.getMessage());
            throw e;
        }
    }

    /**
     * Deletes a track from the database.
     *
     * @param project the project that the track belongs to
     * @param trackId the track id
     */
    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public void deleteTrack(Project project, Long trackId) {
        projectRepository.deleteTrackFromProject(project.getId(), trackId);
        logMessageRepository.deleteAllByTrackId(trackId);
        trackRepository.deleteById(trackId);
    }

    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public void addPlainDataSetToTrack(Track track, PlainData data) {
        trackRepository.addDataSetToTrack(track.getId(), data.getId());
    }


    public TrackDO prepareAllDataSets(Track track, String user) {
        var temp = track.getDataSets().parallelStream().map(data -> {

            List<String> requiredData = switch (data.getDataType()){
                case ML -> getMlData((MlDataSet) data, user);
                case TSA -> getTSAData((TSADataSet) data, user);
                default -> data.calculateData();
            };


            var dataSetDO = new DataSetDO();
            if (data.getDataType().equals(DataTypes.SLEEP)) {
                var sleepDataSet = (SleepDataSet) data;
                dataSetDO.setSleepTime(sleepDataSet.getSleepTime());
            }
            return dataSetDO
                    .setValues(requiredData)
                    .setId(data.getId())
                    .setName(data.getName())
                    .setFrequency(data.getFrequency() != null ? data.getFrequency() : 0)
                    .setPosition(data.getPosition())
                    .setType(data.getDataType());
        }).toList();

        return new TrackDO()
                .setDatasets(temp)
                .setId(track.getId())
                .setName(track.getName())
                .setUnit(track.getUnit())
                .setRepeating(track.isRepeating());
    }

    /**
     * Retrieves TSA data for a given TSA data set and user.
     *
     * @param dataSet the TSA data set from which to retrieve data
     * @param user the user for whom to retrieve data
     * @return a list of strings containing the TSA data
     */
    private List<String> getTSAData(TSADataSet dataSet, String user){
        var config = dataSet.getTsdConfig().getConfiguration();
        var trainData = dataSet.getTsdConfig().getTrainData()
                .stream()
                .map(test -> new TrainDataConfigurationDTO()
                        .setTrainDataId(test.getTrainData().getId())
                        .setConfig(test.getLevelConfig()))
                .toList();

        return restService.callForTSDData(config.getTsdModel().getId(), config.getId(), trainData, user);
    }

    public List<String> getMlData(MlDataSet dataSet, String user){
        var config = dataSet.getMlConfig().getMlConfiguration();

        return switch (dataSet.getMlConfig().getGenerationOption()) {
            case GENERATE -> restService.callForMLData(config.getMlmodel().getId(), config.getId(), user);
            case FORECAST -> restService.callForMLForecast(dataSet, user);
        };
    }

}
