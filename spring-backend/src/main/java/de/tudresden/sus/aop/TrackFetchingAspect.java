package de.tudresden.sus.aop;

import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.repositories.ProjectRepository;
import de.tudresden.sus.adapter.outbound.repositories.UserRepository;
import de.tudresden.sus.ports.TrackServicePort;
import de.tudresden.sus.service.JwtServiceImpl;
import de.tudresden.sus.service.exceptions.ProcessingErrorException;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.util.stream.IntStream;

@Aspect
@Component
@Slf4j
@Order(2)
@RequiredArgsConstructor
public class TrackFetchingAspect {

    private final ProjectRepository projectRepository;
    private final TrackServicePort trackRepository;


    private final HttpServletRequest request;
    private final JwtServiceImpl service;
    private final UserRepository repository;

    @Around("@annotation(fetchTrack)")
    public Object fetchTrackAndProceed(ProceedingJoinPoint joinPoint, FetchTrack fetchTrack) throws Throwable {
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        String[] parameterNames = signature.getParameterNames();
        Object[] args = joinPoint.getArgs();

        var user = extractUserFromJWT();
        if (user == null) {
            throw new ProcessingErrorException("Authorization missing", "UNAUTHORIZED", 403);
        }

        log.info("__________");
        int projectIdIndex = -1;
        int trackIdIndex = -1;
        for (int i = 0; i < parameterNames.length; i++) {
            if (fetchTrack.projectIdArgName().equals(parameterNames[i])) {
                projectIdIndex = i;
            }
            if (fetchTrack.trackIdArgName().equals(parameterNames[i])) {
                trackIdIndex = i;
            }
        }
        log.info("__________");
        log.info("__________ {}  {}", projectIdIndex, trackIdIndex);
        if (projectIdIndex == -1 || trackIdIndex == -1) {
            throw new ProcessingErrorException("track id missing", "T_ID_MIS", 400);
        }

        Long projectId = (Long) args[projectIdIndex];
        Long trackId = (Long) args[trackIdIndex];
        log.info("__________ {}  {}", projectId, trackId);
        var project = projectRepository.findByIdAndUser(projectId, user).orElseThrow(() -> {
            log.error("project not found");
            return new ProcessingErrorException("project not found", "P_ID_MIS", 400);
        });

        if (project == null) {
            throw new ProcessingErrorException("project id missing or null", "P_ID_MIS", 404);
        }

        var track = trackRepository.getTrackForProject(projectId, trackId);
        if (track == null) {
            throw new ProcessingErrorException("track id missing or not found", "T_ID_MIS", 404);
        }

        args[projectIdIndex] = project;
        args[trackIdIndex] = track;

        // Create a new args array without the projectId and trackId
        int finalProjectIdIndex = projectIdIndex;
        int finalTrackIdIndex = trackIdIndex;
        Object[] newArgs = IntStream.range(0, args.length)
                .filter(i -> i != finalProjectIdIndex && i != finalTrackIdIndex)
                .mapToObj(i -> args[i])
                .toArray();

        return joinPoint.proceed(newArgs);
    }

    private User extractUserFromJWT() {
        String authHeader = request.getHeader("Authorization");

        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String jwtToken = authHeader.substring(7);
            return repository.findByEmail(service.extractUserName(jwtToken)).orElse(null);
        }
        return null;
    }
}
