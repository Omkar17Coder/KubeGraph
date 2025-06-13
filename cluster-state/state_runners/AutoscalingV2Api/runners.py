from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class AutoscalingV2Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.AutoscalingV2Api, name)


class HPA_RUNNER(AutoscalingV2Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AutoscalingV2Api_HPAS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_horizontal_pod_autoscaler_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
