package de.tudresden.sus.ports;

import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.adapter.outbound.entity.Track;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface ProjectServicePort {

    List<Project> getAllProjects();
    Project getProjectById(Long id);
    Project createProject(Project project);
    Project updateProject(Long id, Project projectRequest);
    void addTrackToProject(Project project, Track track);
    void deleteProject(Long id);
    void startMessageSending(Project project, String user);
    void stopMessageSending(Project project);
}
