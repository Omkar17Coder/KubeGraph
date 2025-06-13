from abc import ABC,abstractmethod
from email import message
from typing import Self
from kubernetes import watch
from datetime import datetime

from message_format.message_format import MonitoringMessage
from queue_service.In_memory_queue import queue_service
from rich.console import Console

import asyncio


class BaseWatcher(ABC):
    
    def __init__(self,name:str,resource_type:str, base_service) :
        self.console=Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
            )
        self.name=name
        self.resource_type=resource_type
        self.base_service=base_service

    
    async def run(self):
        while True:
            for file in self.base_service.files:
                client = self.base_service.get_client(file)
                if client:
                    try:
                        await self.watch_resources(file, client)
                    except Exception as e:
                        print(f"[red]Error watching {self.resource_type} in {file}: {e}[/red]")
            await asyncio.sleep(60) 
    

    async def watch_resources(self, file, client):
        try:
            loop = asyncio.get_running_loop()
            w = watch.Watch()

            def blocking_stream():
                return w.stream(self.get_watch_stream(client), timeout_seconds=20)

            for event in await loop.run_in_executor(None, lambda: list(blocking_stream())):
                event_type = event["type"]
                resource_obj = event["object"]
                await self.handle_event(file, event_type, resource_obj)

        except Exception as e:
            self.console.print(f"[red] Error in watcher for {self.resource_type} in file {file}: {e}[/red]")

    @staticmethod

    def handle_event(file,event_type,resouce_obj):
        metadata=resouce_obj.get("metadata",{})
        resource_name = metadata.get("name", "unknown")
        Message_namespace = metadata.get("namespace")
        cluster_name = file[:file.find(".")]

        message=MonitoringMessage(
            cluster_name=cluster_name,
            resource_type=self.resource_type,
            resource_name=resource_name,
            namespace=Message_namespace,
            action=event_type,
            timestamp=datetime.now(),
            data=resouce_obj
        )

        asyncio.create_task(queue_service.publish(f"{resource_type}_changes", message.to_json()))


    @abstractmethod

    def get_watch_stream(self,client):
        raise NotImplementedError("Subclass must implement this function")


