package de.tudresden.sus.service;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import de.tudresden.sus.adapter.inbound.dto.PlainDataOccurrenceDTO;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.Track;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata.CharDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata.FileDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.intdata.IntegerDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper.SleepDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSADataSet;
import de.tudresden.sus.adapter.outbound.mapper.DataMapper;
import de.tudresden.sus.adapter.outbound.repositories.PlainDataRepository;
import de.tudresden.sus.adapter.outbound.repositories.ProjectRepository;
import de.tudresden.sus.adapter.outbound.repositories.TrackRepository;
import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import de.tudresden.sus.ports.DataSetServicePort;
import de.tudresden.sus.util.DataReducer;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Objects;


@RequiredArgsConstructor
@Slf4j
@Service
public class DataSetService implements DataSetServicePort {
    @Value(value = "${data-reducer.threshold}")
    private int dataReductionThreshold;
    private final DataReducer dataReducer;
    private final DataMapper mapper;
    private final PlainDataRepository repository;
    private final TrackRepository trackRepository;
    private final ProjectRepository projectRepository;

    /**
     * Returns a dataset from the database for the given id
     *
     * @param id the dataset id
     * @return the dataset object
     */
    public PlainDataDTO findById(Long id) {
        try {
            return repository.findById(id).map(mapper::toDTO).orElseThrow(() -> new EntityNotFoundException("No dataset found for given id"));
        } catch (EntityNotFoundException e) {
            log.error("Entity not found for ID {}: {}", id, e.getMessage());
            throw e;
        }
    }

    /**
     * Returns a dataset belonging to a certain track.
     *
     * @param track     the track
     * @param datasetId the dataset id
     * @return the dataset object
     */
    public PlainDataDTO getDatasetForTrack(Track track, Long datasetId) {
        try {
            return track.getDataSets().stream()
                    .filter(d -> Objects.equals(d.getId(), datasetId))
                    .map(mapper::toDTO).findFirst().orElseThrow(() -> new EntityNotFoundException("No dataset found for track and dataset id"));
        } catch (EntityNotFoundException e) {
            log.error("Entity not found for track_ID {} and dataSetId_{}: {}", track.getId(), datasetId, e.getMessage());
            throw e;
        }
    }

    /**
     * Deletes a dataset from the database
     *
     * @param track the track the dataset belongs to
     * @param dto   the dataset
     */
    public void deleteDataSet(Track track, PlainDataDTO dto) {
        // first break up relation to track
        log.info("deleting dataset: {} for track: {}, remaining datasets: {}", dto.getName(), track.getName(), track.getDataSets().size() - 1);
        // each dataset behind the current one has to move forwards by one
        trackRepository.deleteDataSetFromProject(track.getId(), dto.getId());
        track.getDataSets().forEach(d -> {
            if (d.getPosition() >= dto.getPosition()) {
                d.setPosition(d.getPosition() - 1);
                merge(d);
            }
        });
        repository.deleteById(dto.getId());
    }


    public PlainDataDTO merge(PlainDataDTO dto) {
        var temp = mapper.toEO(dto);
        return mapper.toDTO(merge(temp));
    }

    public PlainData merge(PlainData data) {
       return repository.saveAndFlush( data);
    }


    public JsonNode getPreviewData(PlainData data) {
        return data.calculatePreviewData(dataReductionThreshold, dataReducer);
    }

    @AttachUser
    public List<PlainDataOccurrenceDTO> findAllMlDataSetsForConfigurationId(Long id) {
        User user = UserAspect.getCurrentUser();
        return repository.findAllMlByMLConfigurationId(id, user.getId()).stream().map(row -> {
            Long pId = ((Number) row[0]).longValue();
            Long tId = ((Number) row[1]).longValue();
            Long pdId = ((Number) row[2]).longValue();
            String pName = (String) row[3];
            String tName = (String) row[4];
            String pdName = (String) row[5];
            return new PlainDataOccurrenceDTO(pId, tId, pdId, pName, tName, pdName);
        }).toList();
    }

    @AttachUser
    public List<PlainDataOccurrenceDTO> findAllTSDDataSetsForConfigurationId(Long id) {
        User user = UserAspect.getCurrentUser();
        return repository.findAllTSDByTSDConfigurationId(id, user.getId()).stream().map(row -> {
            Long pId = ((Number) row[0]).longValue();
            Long tId = ((Number) row[1]).longValue();
            Long pdId = ((Number) row[2]).longValue();
            String pName = (String) row[3];
            String tName = (String) row[4];
            String pdName = (String) row[5];
            return new PlainDataOccurrenceDTO(pId, tId, pdId, pName, tName, pdName);
        }).toList();
    }

    public PlainData findByProjectIdAndTrackIdAndPlainDataId(Long projectId, Long trackId, Long plainDataId){
        projectRepository.findById(projectId).orElseThrow(() -> new EntityNotFoundException("No project found"));
        trackRepository.findById(trackId).orElseThrow(() -> new EntityNotFoundException("No track found"));
        return repository.findById(plainDataId).orElseThrow(() -> new EntityNotFoundException("No dataSet found"));
    }
}
