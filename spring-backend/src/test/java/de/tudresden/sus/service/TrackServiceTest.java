package de.tudresden.sus.service;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlConfigData;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.Operation;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.fail;

@ExtendWith(MockitoExtension.class)
public class TrackServiceTest {

    @Mock
    DjangoRestService restService;

    @InjectMocks
    TrackService trackService;

    /**
     * Tests the getMlData method of the TrackService class.
     * Mocks the restService's callForMLData and callForMLForecast methods to return dummy data.
     * Asserts that getMlData returns the expected results when(when called with mocked data sets).
     */
    @Test
    public void testGetMlDataGenerateOption() {
        String user = "User";
        MlDataSet dataSet = new MlDataSet();
        var mlConfig = new MlConfigData();
        mlConfig.setGenerationOption(Operation.GENERATE);
        dataSet.setMlConfig(mlConfig);
        List<String> dummyData = List.of("data1", "data2", "data3");

        when(restService.callForMLData(any(), any(), Mockito.eq(user)))
            .thenReturn(dummyData);

        List<String> result = trackService.getMlData(dataSet, user);
        assertEquals(dummyData, result);
    }

    @Test
    public void testGetMlDataForecastOption() {
        String user = "User";
        MlDataSet dataSet = new MlDataSet();
        var mlConfig = new MlConfigData();
        mlConfig.setGenerationOption(Operation.FORECAST);
        dataSet.setMlConfig(mlConfig);
        List<String> dummyData = List.of("data1", "data2", "data3");

        when(restService.callForMLForecast(any(), Mockito.eq(user)))
            .thenReturn(dummyData);

        List<String> result = trackService.getMlData(dataSet, user);
        assertEquals(dummyData, result);
    }

}