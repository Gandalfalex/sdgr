package de.tudresden.sus.service;

import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.adapter.outbound.entity.Track;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.repositories.ProjectRepository;
import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import de.tudresden.sus.datagenerator.sender.ThreadOrganizer;
import de.tudresden.sus.ports.ProjectServicePort;
import de.tudresden.sus.ports.TrackServicePort;
import de.tudresden.sus.util.ProjectTopicNameBuilder;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.ExecutionException;

@Service
@RequiredArgsConstructor
@Slf4j
public class ProjectService implements ProjectServicePort{

    private final ProjectRepository projectRepository;
    private final TrackServicePort trackService;
    private final KafkaAdmin kafkaAdmin;
    @Value(value="${spring.kafka.bootstrap-topic}")
    private String topicName;

    private final ThreadOrganizer threadOrganizer;

    /**
     * Returns all project in the database.
     *
     * @return the list of projects
     */

    public List<Project> getAllProjects() {
        return projectRepository.findAll();
    }

    /**
     * Returns a project object from its id.
     *
     * @param id the project id
     * @return the project object
     */
    public Project getProjectById(Long id) {
        try {
            return projectRepository.findById(id).orElseThrow(() -> new EntityNotFoundException("project does not exist"));
        } catch (EntityNotFoundException e) {
            log.error("Entity not found for ID {}: {}", id, e.getMessage());
            throw e;
        }
    }

    /**
     * Creates a project in the database.
     *
     * @param project the new project
     * @return the persisted object
     */
    @AttachUser
    public Project createProject(Project project) {
        User user = UserAspect.getCurrentUser();
        log.info("{} saved, ", project.toString());

        project.setUser(user);
        var savedProject = projectRepository.save(project);

        try (AdminClient adminClient = AdminClient.create(kafkaAdmin.getConfigurationProperties())) {
            var newTopic = new NewTopic(ProjectTopicNameBuilder.buildTopicName(savedProject.getId()), 1, (short) 1);
            adminClient.createTopics(List.of(newTopic)).all().get();
        } catch (Exception e) {
            throw new RuntimeException("Failed to create topic " + topicName, e);
        }

        return savedProject;
    }

    /**
     * Updates a project in the database.
     *
     * @param id             the id of the project to update
     * @param projectRequest the new project data
     * @return the updated project
     */
    public Project updateProject(Long id, Project projectRequest) {
        Project project = projectRepository.findById(id).orElseThrow(() -> {
            log.error("project with id {} not found", id);
            return new EntityNotFoundException("No project found for given id");
        });
        log.info("found {} new tracks", projectRequest.getTracks().size() - project.getTracks().size());
        project.setTracks(project.getTracks());
        project.setName(projectRequest.getName());
        return projectRepository.save(project);
    }

    public void addTrackToProject(Project project, Track track) {
        projectRepository.addTrackToProject(project.getId(), track.getId());
    }

    /**
     * Deletes a project from the database.
     *
     * @param id the project id
     */
    public void deleteProject(Long id) {
        try {
            Project project = projectRepository.findById(id).orElseThrow(() -> new EntityNotFoundException("No project found for given id"));
            projectRepository.delete(project);
            AdminClient adminClient = AdminClient.create(kafkaAdmin.getConfigurationProperties());
            adminClient.deleteTopics(List.of(ProjectTopicNameBuilder.buildTopicName(id))).all().get();
        } catch (EntityNotFoundException e) {
            log.error("Project entity not found for ID {}: {}", id, e.getMessage());
            throw e;
        } catch (ExecutionException | InterruptedException e) {
            log.error("Failed to delete topic {}", topicName, e);
            throw new RuntimeException(e);
        }
    }

    /**
     * start sending messages for project
     *
     * @param project
     */
    public void startMessageSending(Project project, String user) {
        log.info("project: {}", project);
        project.getTracks().forEach(track -> {
            var trackDO = trackService.prepareAllDataSets(track, user);
            log.info("track {} starts sending messages", track.getId());
            threadOrganizer.runConfigDataSetThreads(trackDO, project.getId());
        });
    }

    /**
     * stop sending messages for project
     *
     * @param project
     */
    public void stopMessageSending(Project project) {
        log.info("stop sending messages");
        threadOrganizer.stopThreads(project.getId());
    }
}
