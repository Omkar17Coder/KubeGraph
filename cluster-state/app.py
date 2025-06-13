from state_runners.CoreV1Api.runners import (
    POD_RUNNER,
    NAMESPACE_RUNNER,
    CONFIGMAP_RUNNER,
    COMPONENT_STATUS_RUNNER,
    ENDPOINT_RUNNER,
    EVENT_RUNNER,
    LIMIT_RANGE_RUNNER,
    NODE_RUNNER,
    PVC_RUNNER,
    PV_RUNNER,
    POD_TEMPLATE_RUNNER,
    REPLICATION_CONTROLLER_RUNNER,
    RESOURCE_QUOTA_RUNNER,
    SECRET_RUNNER,
    SERVICE_ACCOUNT_RUNNER,
    SERVICE_RUNNER,
)
import asyncio


class APP:
    def __init__(self) -> None:
        self.STATE_OBJECTS = {
            "POD_TEMPLATE_RUNNER": POD_RUNNER(),
            "NAMESPACE": NAMESPACE_RUNNER(),
            "CONFIGMAP_RUNNER": CONFIGMAP_RUNNER(),
            "COMPONENT_STATUS_RUNNER": COMPONENT_STATUS_RUNNER(),
            "ENDPOINT_RUNNER": ENDPOINT_RUNNER(),
            "EVENT_RUNNER": EVENT_RUNNER(),
            "LIMIT_RANGE_RUNNER": LIMIT_RANGE_RUNNER(),
            "NODE_RUNNER": NODE_RUNNER(),
            "PV_RUNNER": PV_RUNNER(),
            "PVC_RUNNER": PVC_RUNNER(),
            "POD_TEMPLATE_RUNNER": POD_TEMPLATE_RUNNER(),
            "REPLICATION_CONTROLLER_RUNNER": REPLICATION_CONTROLLER_RUNNER(),
            "RESOURCE_QUOTA_RUNNER": RESOURCE_QUOTA_RUNNER(),
            "SECRET_RUNNER": SECRET_RUNNER(),
            "SERVICE_RUNNER": SERVICE_RUNNER(),
            "SERVICE_ACCOUNT_RUNNER": SERVICE_ACCOUNT_RUNNER(),
        }

    async def run(self) -> None:
        await asyncio.gather(*[self.STATE_OBJECTS[_].run() for _ in self.STATE_OBJECTS])


if __name__ == "__main__":
    print("Starting app")
    APPLICATION = APP()
    asyncio.run(APPLICATION.run())
