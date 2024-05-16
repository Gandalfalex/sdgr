package de.tudresden.sus.adapter.outbound.restclient;


public interface DjangoRestClientURLBuilder {

    String ML_ENDPOINT = "ML/";
    String TSA_ENDPOINT = "TSA/";

    default String getConfigurationForMLModelURL(String baseURL, Long ml_model, Long configId){
        return String.format("/ml/ml_model/%d/ml_solution/%d/ml_configuration/load_data", ml_model, configId);
    }

    default String getConfigurationFromTSDModelURL(String baseURL, Long modelId, Long configId){
        return String.format("http://%s/tsd/tsd_model/%d/tsd_configuration/%d/configure",baseURL, modelId, configId);
    }
}
