from state_runners.base.base_runner import BASE_RUNNER
from kubernetes.watch import Watch
from kubernetes import client


class CoreV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name:str,resource_type:str) -> None:
        super().__init__(client.CoreV1Api, name,resource_type)


class POD_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PODS","pod")

    def get_watch_stream(self, client_obj):
        return  client_obj.list_pod_for_all_namespaces

class NODE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NODES", "node")

    def get_watch_stream(self, client):
        return client.list_node


class NAMESPACE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NAMESPACES", "namespace")

    def get_watch_stream(self, client):
        return client.list_namespace



class SERVICE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICES", "service")

    def get_watch_stream(self, client):
        return client.list_service_for_all_namespaces

class ENDPOINT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_ENDPOINTS", "endpoints")

    def get_watch_stream(self, client):
        return client.list_endpoints_for_all_namespaces

class SECRET_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SECRETS", "secret")

    def get_watch_stream(self, client):
        return client.list_secret_for_all_namespaces

class PVC_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVCS", "persistentvolumeclaim")

    def get_watch_stream(self, client):
        return client.list_persistent_volume_claim_for_all_namespaces

class PV_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVS", "persistentvolume")

    def get_watch_stream(self, client):
        return client.list_persistent_volume

class COMPONENT_STATUS_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_COMPONENT_STATUS", "componentstatus")

    def get_watch_stream(self, client):
        return client.list_component_status

class LIMIT_RANGE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_LIMIT_RANGES", "limitrange")

    def get_watch_stream(self, client):
        return client.list_limit_range_for_all_namespaces

class RESOURCE_QUOTA_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_RESOURCE_QUOTAS", "resourcequota")

    def get_watch_stream(self, client):
        return client.list_resource_quota_for_all_namespaces

class EVENT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_EVENTS", "event")

    def get_watch_stream(self, client):
        return client.list_event_for_all_namespaces

class SERVICE_ACCOUNT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICE_ACCOUNTS", "serviceaccount")

    def get_watch_stream(self, client):
        return client.list_service_account_for_all_namespaces

class REPLICATION_CONTROLLER_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_REPLICATION_CONTROLLER", "replicationcontroller")

    def get_watch_stream(self, client):
        return client.list_replication_controller_for_all_namespaces

class POD_TEMPLATE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_POD_TEMPLATE", "podtemplate")

    def get_watch_stream(self, client):
        return client.list_pod_template_for_all_namespaces




############################################### All the below implmentation needs changes###############################



class NAMESPACE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NAMESPACES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_namespace(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class COMPONENT_STATUS_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_COMPONENT_STATUSES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_component_status(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class CONFIGMAP_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_CONFIGMAPS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_config_map_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class ENDPOINT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_ENDPOINTS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_endpoints_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class EVENT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_EVENTS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_event_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class LIMIT_RANGE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_LIMIT_RANGES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_limit_range_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class NODE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NODES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_node(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class PV_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_persistent_volume(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class PVC_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVCS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_persistent_volume_claim_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class POD_TEMPLATE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_POD_TEMPLATES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_pod_template_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class REPLICATION_CONTROLLER_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_REPLICATION_CONTROLLERS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_replication_controller_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class RESOURCE_QUOTA_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_RESOURCE_QUOTAS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_resource_quota_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class SECRET_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SECRETS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_secret_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class SERVICE_ACCOUNT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICE_ACCOUNTS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_service_account_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class SERVICE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_service_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )