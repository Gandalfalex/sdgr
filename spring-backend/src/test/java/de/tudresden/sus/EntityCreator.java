package de.tudresden.sus;

import org.springframework.stereotype.Component;

@Component
public class EntityCreator extends AbstractSusTest {

//    @Resource
//    private DataSetRepository dataSetRepository;
//
//    @Resource
//    private ProjectRepository projectRepository;
//
//    /**
//     * clear database after run, otherwise some elements might still exist and fail the test
//     */
//    @Transactional(Transactional.TxType.REQUIRES_NEW)
//    public void setUp(){
//        projectRepository.deleteAll();
//        dataSetRepository.deleteAll();
//    }
//
//    @Transactional(Transactional.TxType.REQUIRES_NEW)
//    public DataSet createDataSet(String name) {
//        var trend = new LinearTrend();
//        var season = new NoSeason();
//        var residual = new NoResidual();
//
//        return dataSetRepository.saveAndFlush(new DataSet()
//                .setName(name)
//                .setTrend(trend)
//                .setSeason(season)
//                .setResidual(residual));
//    }
//
//    @Transactional(Transactional.TxType.REQUIRES_NEW)
//    public DataSet createDataSet(String name, Residual residual, Season season, Trend trend) {
//        return dataSetRepository.saveAndFlush(new DataSet()
//                .setName(name)
//                .setTrend(trend)
//                .setSeason(season)
//                .setResidual(residual));
//    }
//
//    @Transactional(Transactional.TxType.REQUIRES_NEW)
//    public Project createProject(String name){
//        var project = new Project().setName(name)
//                .setDataSets(List.of(createDataSetWithoutSaving("Set1"), createDataSetWithoutSaving("Set2")));
//        projectRepository.saveAndFlush(project);
//        return project;
//    }
//
//    @Transactional(Transactional.TxType.REQUIRES_NEW)
//    public Project createProject(List<DataSet> dataSets, String name) {
//        var project = new Project().setName(name).setDataSets(dataSets);
//        projectRepository.saveAndFlush(project);
//        return project;
//    }
//
//    @Transactional(Transactional.TxType.REQUIRES_NEW)
//    public DataSet createDataSetWithoutSaving(String name){
//        return new DataSet()
//                .setName(name)
//                .setResidual(new NoResidual())
//                .setSeason(new NoSeason())
//                .setTrend(new LinearTrend());
//    }

}
