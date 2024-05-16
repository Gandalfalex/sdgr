package de.tudresden.sus.adapter.inbound.rest;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import de.tudresden.sus.adapter.inbound.dto.ProjectDTO;
import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.FetchProject;
import de.tudresden.sus.aop.UserAspect;
import de.tudresden.sus.datagenerator.sender.ThreadOrganizer;
import de.tudresden.sus.ports.ProjectServicePort;
import de.tudresden.sus.security.authentification.RestError;
import de.tudresden.sus.service.ProjectService;
import io.micrometer.core.annotation.Timed;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/projects")
@Slf4j
@RequiredArgsConstructor
public class ProjectController {

    private final ProjectServicePort projectService;
    private final ObjectMapper objectMapper;
    private final ThreadOrganizer threadOrganizer;


    @GetMapping
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return all projects",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = ProjectDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid tsd model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getAllProjects.time", description = "Time taken to get all projects")
    @AttachUser
    public List<ProjectDTO> getAllProjects() {
        User user = UserAspect.getCurrentUser();
        log.info("searching for projects of user: {}", user.getEmail());
        return projectService.getAllProjects().stream().map(this::toDTO).toList();
    }

    @GetMapping("/{id}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "given an id, return the corresponding project",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = ProjectDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid tsd model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getProjectById.time", description = "Time taken to get project by id")
    public ResponseEntity<ProjectDTO> getProjectById(@PathVariable Long id) {
        var project = projectService.getProjectById(id);
        var response = toDTO(project);
        return ResponseEntity.ok(response);
    }

    /**
     * New project has no datasets. To create project with datasets, use the upload endpoint to upload a config.
     */
    @PostMapping
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "201",
                            description = "create a new project",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = ProjectDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid tsd model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "createNewProject.time", description = "Time taken to create new project")
    public ResponseEntity<ProjectDTO> createNewProject(@Valid  @RequestBody ProjectDTO projectDTO) {
        var request = toEO(projectDTO);

        var project = projectService.createProject(request);
        var response = toDTO(project);

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "update a project",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = ProjectDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid tsd model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "updateProject.time", description = "Time taken to update project")
    public ResponseEntity<ProjectDTO> updateProject(@PathVariable long id, @Valid @RequestBody ProjectDTO projectDTO) {
        var request = toEO(projectDTO);

        var project = projectService.updateProject(id, request);
        var response = toDTO(project);

        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "204",
                            description = "delete a project given its id"
                    )
            }
    )
    @Timed(value = "deleteProject.time", description = "Time taken to delete project")
    public ResponseEntity<ProjectDTO> deleteProject(@PathVariable long id) {
        projectService.deleteProject(id);

        return ResponseEntity.noContent().build();
    }

    @GetMapping("/{id}/download")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "download the project config",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(type = "file")
                            )
                    )
            }
    )
    @Timed(value = "downloadProject.time", description = "Time taken to download project")
    public ResponseEntity<Resource> downloadProject(@PathVariable long id) throws JsonProcessingException {
        var project = projectService.getProjectById(id);

        var jsonBytes = objectMapper.writeValueAsBytes(project);
        var resource = new ByteArrayResource(jsonBytes);

        var headers = new HttpHeaders();
        headers.add(HttpHeaders.CACHE_CONTROL, "no-cache, no-store, must-revalidate");
        headers.add(HttpHeaders.PRAGMA, "no-cache");
        headers.add(HttpHeaders.EXPIRES, "0");
        headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"config.json\"");

        return ResponseEntity.ok()
                .headers(headers)
                .contentLength(resource.contentLength())
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(resource);
    }

    @PostMapping("/upload")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "201",
                            description = "upload the project config",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = ProjectDTO.class)
                            )
                    )
            }
    )
    @Timed(value = "uploadProject.time", description = "Time taken upload project")
    public ResponseEntity<ProjectDTO> uploadProject(@RequestParam MultipartFile file) throws IOException {
        log.info("file = {}", file);
        var fileContent = new String(file.getBytes());
        var request = objectMapper.readValue(fileContent, Project.class);


        var project = projectService.createProject(request);
        var response = toDTO(project);

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    private Project toEO(ProjectDTO dto) {
        return new Project().setId(dto.getId()).setName(dto.getName());
    }

    private ProjectDTO toDTO(Project project) {
        return new ProjectDTO().setName(project.getName()).setId(project.getId()).setSending(threadOrganizer.checkIfRunning(project.getId()));
    }
}
