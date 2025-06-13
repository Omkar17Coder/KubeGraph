from kubernetes import client
from kubernetes.watch import Watch
from state_runners.base.base_runner import BASE_RUNNER


class DEPLOYMENT_RUNNER(BASE_RUNNER):
    def __init__(self, namespace="default"):
        super().__init__(client.AppsV1Api, "deployment", {"namespace": namespace})

    def get_watch_stream(self, client):
        return Watch().stream(client.list_namespaced_deployment, namespace=self.watch_args["namespace"], timeout_seconds=60)


class STATEFULSET_RUNNER(BASE_RUNNER):
    def __init__(self, namespace="default"):
        super().__init__(client.AppsV1Api, "statefulset", {"namespace": namespace})

    def get_watch_stream(self, client):
        return Watch().stream(client.list_namespaced_stateful_set, namespace=self.watch_args["namespace"], timeout_seconds=60)


class DAEMONSET_RUNNER(BASE_RUNNER):
    def __init__(self, namespace="default"):
        super().__init__(client.AppsV1Api, "daemonset", {"namespace": namespace})

    def get_watch_stream(self, client):
        return Watch().stream(client.list_namespaced_daemon_set, namespace=self.watch_args["namespace"], timeout_seconds=60)


class REPLICASET_RUNNER(BASE_RUNNER):
    def __init__(self, namespace="default"):
        super().__init__(client.AppsV1Api, "replicaset", {"namespace": namespace})

    def get_watch_stream(self, client):
        return Watch().stream(client.list_namespaced_replica_set, namespace=self.watch_args["namespace"], timeout_seconds=60)
