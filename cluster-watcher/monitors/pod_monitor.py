from state_runners.base.base_watcher import BaseWatcher
from kubernetes  import client

class PodMonitor(BaseWatcher):
    def __init__(self, name: str,  base_service):
        super().__init__("PodMonitor","pod",base_service)

    def get_watch_stream(self, client):
        return client.list_pod_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )