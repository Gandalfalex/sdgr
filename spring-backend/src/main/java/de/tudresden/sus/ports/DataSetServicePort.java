package de.tudresden.sus.ports;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import de.tudresden.sus.adapter.inbound.dto.PlainDataOccurrenceDTO;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.Track;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface DataSetServicePort {
    PlainDataDTO findById(Long id);

    PlainDataDTO getDatasetForTrack(Track track, Long datasetId);

    void deleteDataSet(Track track, PlainDataDTO dto);

    PlainDataDTO merge(PlainDataDTO dto);

    PlainData merge(PlainData data);

    JsonNode getPreviewData(PlainData data);

    List<PlainDataOccurrenceDTO> findAllMlDataSetsForConfigurationId(Long id);

    List<PlainDataOccurrenceDTO> findAllTSDDataSetsForConfigurationId(Long id);

    PlainData findByProjectIdAndTrackIdAndPlainDataId(Long projectId, Long trackId, Long plainDataId);
}
