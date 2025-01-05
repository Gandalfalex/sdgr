package de.tudresden.sus.util;

public class ProjectTopicNameBuilder {
    public static String buildTopicName(Long projectId) {
        return "project-" + projectId;
    }
}
