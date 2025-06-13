import asyncio
import os
from rich.console import Console
from queue_service import queue_service
from state_runners.CoreV1Api import (
    POD_RUNNER, NODE_RUNNER, CONFIGMAP_RUNNER
)
from message_format.message_format import MonitoringMessage
from state_runners.AppsV1Api import (
    DEPLOYMENT_RUNNER, STATEFULSET_RUNNER, DAEMONSET_RUNNER, REPLICASET_RUNNER
)

KUBECONFIG_DIR = "./kubeconfigs"
SUBSCRIBED_CLUSTERS = set()
console = Console()

# -------------------- Runners --------------------
RUNNERS = {
    "POD_RUNNER": POD_RUNNER(namespace="default"),
    "NODE_RUNNER": NODE_RUNNER(),
    "CONFIGMAP_RUNNER": CONFIGMAP_RUNNER(namespace="default"),
    "DEPLOYMENT_RUNNER": DEPLOYMENT_RUNNER(namespace="default"),
    "STATEFULSET_RUNNER": STATEFULSET_RUNNER(namespace="default"),
    "DAEMONSET_RUNNER": DAEMONSET_RUNNER(namespace="default"),
    "REPLICASET_RUNNER": REPLICASET_RUNNER(namespace="default"),
}


# -------------------- Handler --------------------
async def handle_event(message: MonitoringMessage):
    console.log(f"[cyan]Received message:[/cyan] {message}")


# -------------------- Dynamic Subscription --------------------
async def monitor_kubeconfig_and_subscribe():
    while True:
        current_files = set(os.listdir(KUBECONFIG_DIR))
        new_files = current_files - SUBSCRIBED_CLUSTERS

        for file in new_files:
            if not file.endswith(".yaml"):
                continue

            cluster_name = file.split(".")[0]
            channel = f"{cluster_name}_changes"

            await queue_service.subscribe(channel, handle_event)
            SUBSCRIBED_CLUSTERS.add(file)
            console.log(f"[green]Subscribed to {channel}[/green]")

        await asyncio.sleep(30)  

# -------------------- Main --------------------
async def main():
    runner_tasks = [asyncio.create_task(r.run()) for r in RUNNERS.values()]
    subscriber_task = asyncio.create_task(monitor_kubeconfig_and_subscribe())

    await asyncio.gather(*runner_tasks, subscriber_task)


if __name__ == "__main__":
    asyncio.run(main())
