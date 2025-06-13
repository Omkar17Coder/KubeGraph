from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class CertificatesV1alpha1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.CertificatesV1alpha1Api, name)


class CLUSTER_TRUST_BUNDLE_RUNNER(CertificatesV1alpha1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CertificatesV1alpha1Api_CLUSTER_TRUST_BUNDLES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_cluster_trust_bundle(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
