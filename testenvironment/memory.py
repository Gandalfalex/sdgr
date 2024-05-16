import os
import time

import psutil


class MemoryMonitor:
    def __init__(self):
        self.keep_measuring = True
        self.max_memory = 0

    def measure_memory(self):
        process = psutil.Process(os.getpid())
        while self.keep_measuring:
            memory = process.memory_info().rss / (1024.0 ** 2)  # Convert from bytes to MB
            if memory > self.max_memory:
                self.max_memory = memory
            time.sleep(1)