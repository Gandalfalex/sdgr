package de.tudresden.sus.aop;

import de.tudresden.sus.ports.ProjectServicePort;
import de.tudresden.sus.service.ProjectService;
import de.tudresden.sus.service.exceptions.ProcessingErrorException;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class ProjectFetchAspect {

    @Autowired
    private ProjectServicePort projectService;

    @Around("@annotation(fetchProject)")
    public Object fetchProjectAndProceed(ProceedingJoinPoint joinPoint, FetchProject fetchProject) throws Throwable {
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        String[] parameterNames = signature.getParameterNames();
        Object[] args = joinPoint.getArgs();

        int projectIdIndex = -1;
        for (int i = 0; i < parameterNames.length; i++) {
            if (fetchProject.projectIdArgName().equals(parameterNames[i])) {
                projectIdIndex = i;
                break;
            }
        }


        if (projectIdIndex == -1) {
            throw new ProcessingErrorException("project id missing", "P_ID_MIS", 400);
        }

        Long projectId = (Long) args[projectIdIndex];
        var project = projectService.getProjectById(projectId);
        if (project == null) {
            throw new ProcessingErrorException("project does not exist", "P_ID_IV", 404);
        }

        args[projectIdIndex] = project;
        return joinPoint.proceed(args);
    }
}
