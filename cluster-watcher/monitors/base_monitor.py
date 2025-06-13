from abc import ABC ,abstractmethod
from multiprocessing.connection import Client

from rich.console import Console
import _asyncio
import os 
import time
from datetime import datetime
from typing import Dict,Any,Optional

from constants.constants import KUBECONF_PATH
from kubeconfig_utils.utils import  get_api_client
from  message_format.message_format import MonitoringMessage
from queue_service.In_memory_queue import queue_service



class BaseMonitor(ABC):
    def __init__(self,name:str,resource_type:str):
        self.console=Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,

        )
        self.name=name
        self.resource_type=resource_type
        self.previous_state={}
        self.current_state={}

    def load_clients(self)->None:
        self.console.print(f"Loading clients for {self.name}")
        self.api_clients={}
        self.clients={}
        self.files=os.listdir(KUBECONF_PATH)

        to_be_removed=[] ## resources to be removed.

        for file in self.files:
            try:
                self.api_clients[file]=get_api_client(os.path.join(KUBECONF_PATH,file))
                self.clients[file]=self.create_client(self.api_clients[file])

            except Exception as e:
                self.console.print(f"[red] failed to load the config file {file}: {e} [/red]")
                to_be_removed.append(file)

        for file in to_be_removed:
            if file in self.files:
                self.files.remove(file)
        
        self.console.print(f"Loaded {len(self.clients)} clients for {self.name}")

    @abstractmethod
    def create_client(self,api_client):
        "abstract method to create the  kubernetest client"
        raise NotImplementedError("Subclass must implement the function")
    

    def watch_resources(self,api_client):
        "abstract method to create a   watch resource agent"
        raise NotImplementedError("Subclass must implement the function")
    

    async def run(self):
        while True:
            try:
                self.load_clients()
                await self.watch_resources()
            
            except Exception as e:
                self.console.print(f"[red]Error in monitoring {self.name} monitor {e}[/red]")
                time.sleep(10)
                # Sleep 10 sec before retry again.
    

    
    