from abc import ABC, abstractmethod
from rich.console import Console
from kubernetes import watch
import asyncio
import os
import time
from datetime import datetime

import constants.constants as CONSTANTS
import kubeconfig_utils.utils as KUBECONFIG_UTILS
from message_format.message_format import MonitoringMessage
from queue_service.In_memory_queue import queue_service


class BASE_RUNNER(ABC):
    def __init__(self, api_object_class, resource_type:str,watch_args:dict=None) -> None:
        self.RICH_CONSOLE = Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
        )
        self.API_OBJECT_CLASS = api_object_class  ## this is the api object class and we need to use this.

        
        self.RESOURCE_TYPE=resource_type

        self.WATCH_ARGS=watch_args or {}





    def load_clients(self) -> None:
        self.RICH_CONSOLE.print(f"Loading kubeconfigs for [cyan]{self.NAME}[/cyan]")
        self.API_CLIENTS = {}
        self.FILES = os.listdir(CONSTANTS.KUBECONF_PATH)

        to_be_removed = []

        for file in self.FILES:
            try:
                self.API_CLIENTS[file] = KUBECONFIG_UTILS.get_api_client(
                    os.path.join(CONSTANTS.KUBECONF_PATH, file)
                )
            except Exception as e:
                self.RICH_CONSOLE.log(f"[red]Failed to load API client for {file}: {e}[/red]")
                to_be_removed.append(file)

        self.CLIENTS = {}
        for file in self.API_CLIENTS:
            try:
                self.CLIENTS[file] = self.API_OBJECT_CLASS(api_client=self.API_CLIENTS[file])
            except Exception as e:
                self.RICH_CONSOLE.log(f"[red]Failed to create API object for {file}: {e}[/red]")
                if file not in to_be_removed:
                    to_be_removed.append(file)

        for file in to_be_removed:
            self.FILES.remove(file)

        self.RICH_CONSOLE.print(f"[green]Loaded kubeconfigs for {self.NAME}[/green]")

    async def run(self) -> None:
        while True:
            self.load_clients()
            await asyncio.sleep(2)

            tasks = []
            for file in self.FILES:
                client = self.CLIENTS.get(file)
                if client:
                    tasks.append(asyncio.create_task(self.watch_cluster(file, client)))

            await asyncio.gather(*tasks)

            if self.need_file_reload():
                self.RICH_CONSOLE.print(f"[yellow]Reloading kubeconfig files for {self.NAME}[/yellow]")
                continue

            await asyncio.sleep(10)

    async def watch_cluster(self, file: str, client) -> None:
        cluster_name = file[:file.find(".")]
        try:
            w = Watch()
            stream = self.get_watch_stream(client)
            for event in stream:
                event_type = event["type"]
                obj = event["object"].to_dict()
                await self.handle_event(cluster_name, event_type, obj)
        except Exception as e:
            self.console.print(f"[red]Error watching {self.resource_type} in {file}: {e}[/red]")
    


    async def handle_event(self, cluster, event_type, resource_obj):
        metadata = resource_obj.get("metadata", {})
        message = MonitoringMessage(
            cluster_name=cluster,
            resource_type=self.resource_type,
            resource_name=metadata.get("name", "unknown"),
            namespace=metadata.get("namespace"),
            action=event_type,
            timestamp=datetime.now(),
            data=resource_obj,
        )
        await queue_service.publish(f"{cluster}_changes", message.to_json())

    def need_file_reload(self) -> bool:
        return sorted(self.FILES) != sorted(os.listdir(CONSTANTS.KUBECONF_PATH))

    def logtime(self) -> str:
        return datetime.now().strftime("[ %Y-%m-%d %H:%M:%S ]")

    @abstractmethod
    def get_watch_stream(self, client):
        raise NotImplementedError("Subclasses must implement get_watch_stream()")
