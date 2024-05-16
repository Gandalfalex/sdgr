package de.tudresden.sus.datagenerator.sender;


import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Service class for managing SendDataThreads in a singleton scope.
 * Tracks and controls the execution of threads associated with specific IDs.
 */
@Service
@Scope("singleton")
@Slf4j
public class ThreadHolder implements PropertyChangeListener {

    private static final Map<Long, ConcurrentLinkedQueue<SendDataThread>> runningThreads = new TreeMap<>();

    /**
     * Starts a SendDataThread and adds it to the tracking map.
     * Threads are tracked based on a unique identifier (UUID).
     *
     * @param thread The SendDataThread to be started and tracked.
     */
    public void startThread(SendDataThread thread) {
        thread.addPropertyChangeListener(this);
        thread.start();
        if (runningThreads.containsKey(thread.getUuid())) {
            runningThreads.get(thread.getUuid()).add(thread);
        } else {
            ConcurrentLinkedQueue<SendDataThread> list = new ConcurrentLinkedQueue<>();
            list.add(thread);
            runningThreads.put(thread.getUuid(), list);
        }
        log.debug("started thread {}", thread.getName());
    }

    /**
     * Handles property change events from SendDataThreads.
     * Removes the thread from the tracking map upon completion or interruption.
     *
     * @param evt The property change event, which includes details about the thread state change.
     */
    @Override
    public void propertyChange(PropertyChangeEvent evt) {
        SendDataThread thread = (SendDataThread) evt.getNewValue();
        if (runningThreads.containsKey(thread.getUuid()))
            runningThreads.get(thread.getUuid()).remove(thread);
        thread.removePropertyChangeListener(this);
    }

    /**
     * Stops all threads associated with a given UUID.
     * Interrupts and removes all threads for the specified UUID from the tracking map.
     *
     * @param uuid The unique identifier of the threads to be stopped.
     */
    public void stopThreads(long uuid) {
        log.debug("thread map before stop of {}: {}", uuid, runningThreads);
        if (runningThreads.containsKey(uuid)) {
            runningThreads.get(uuid).forEach(SendDataThread::interrupt);
            runningThreads.get(uuid).forEach(SendDataThread::interrupt);
            runningThreads.remove(uuid);
        }
        log.debug("thread map after stop of {}: {}", uuid, runningThreads);
    }

    /**
     * Checks if there are any running threads for a given project ID.
     *
     * @param project The project ID to check for running threads.
     * @return true if there are running threads associated with the project, false otherwise.
     */
    public static boolean isRunning(Long project) {
        return runningThreads.containsKey(project);
    }
}
