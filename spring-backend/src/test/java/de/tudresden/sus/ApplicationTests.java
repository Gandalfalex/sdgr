package de.tudresden.sus;

import de.tudresden.sus.adapter.outbound.mapper.DataMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSet;
import de.tudresden.sus.service.DataSetService;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.NoResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies.NoSeason;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.CustomFormulaTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.LinearTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.NoTrend;
import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.service.ProjectService;
import de.tudresden.sus.adapter.outbound.entity.Track;
import de.tudresden.sus.adapter.outbound.repositories.TrackRepository;
import de.tudresden.sus.service.TrackService;
import lombok.RequiredArgsConstructor;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.*;

import static org.junit.jupiter.api.Assertions.assertEquals;
@RequiredArgsConstructor

class ApplicationTests extends AbstractSusTest {

	@Autowired
	ProjectService projectService;

	@Autowired
	TrackService trackService;

	@Autowired
	TrackRepository trackRepository;

	@Autowired
	DataSetService dataSetService;

	private final DataMapper dataMapper;

	@Test
	void contextLoads() {

	}

	@Test
	void testPersistProjectStructure() {
		var dataSet = new FloatDataSet();
		dataSet.setName("dataSet");
		dataSet.setNumSamples(5);
		dataSet.setFrequency(1.0f);
		//dataSet.setTrend(new LinearTrend().setSlope(1).setOffset(0));
		//dataSet.setSeason(new NoSeason());
		//dataSet.setResidual(new NoResidual());

		var track = new Track();
		track.setName("first");
		track.setUnit("V");
		track.setRepeating(true);
		track.setDataSets(new HashSet<>(List.of(dataSet)));

		var project = new Project();
		project.setName("test");
		project.setTracks(new HashSet<>(List.of(track)));

		// persist project
		projectService.createProject(project);

		/* ============================
		   verify structure in database
		   ============================ */

		var projects = projectService.getAllProjects();
		assertEquals(1, projects.size(), "number of projects in the database does not match");

		var tracks = new ArrayList<>(projects.get(0).getTracks());
		assertEquals(1, tracks.size(), "number of tracks in the project does not match");

		var first = tracks.get(0);
		assertEquals(1, first.getDataSets().size(), "number of datasets in the first track does not match");
	}

	@Test
	void testCustomFormulaEvaluator() {
		var formulaTrend = new CustomFormulaTrend();
		formulaTrend.setFormula("2*x^2+4*x-7");

		var x = 5;
		var evaluatedResult = formulaTrend.getValue(x, false);
		var expectedResult = (double) 2 * x*x + 4 * x - 7;
		assertEquals(expectedResult, evaluatedResult, "evaluated result doesn't match the expected result");
	}

	@Test
	void testDeleteDataSetFromTrack() {
		var dataSet = new FloatDataSet();
		dataSet.setName("dataSet");
		//dataSet.setTrend(new NoTrend());
		//dataSet.setSeason(new NoSeason());
		//dataSet.setResidual(new NoResidual());

		var track = new Track();
		track.setName("testTrack");
		track.setUnit("test");
		track.setDataSets(new HashSet<>(List.of(dataSet)));

		// persist track
		trackService.createTrack(track);

		// verify that the track is persisted and has a dataset
		var tracks = trackRepository.findAll();
		assertEquals(1, tracks.size(), "number of tracks in the database doesn't match expected value");

		var dbTrack = tracks.get(0);
		assertEquals(1, dbTrack.getDataSets().size());

		var dbDataSet = new ArrayList<>(dbTrack.getDataSets()).get(0);

		// delete dataSet
		dataSetService.deleteDataSet(track, dataMapper.toDTO(dbDataSet));

		// verify that the track still exists but has no dataset anymore
		tracks = trackRepository.findAll();
		assertEquals(1, tracks.size(), "number of tracks in the database doesn't match expected value");

		dbTrack = tracks.get(0);
		assertEquals(0, dbTrack.getDataSets().size());
	}

}
