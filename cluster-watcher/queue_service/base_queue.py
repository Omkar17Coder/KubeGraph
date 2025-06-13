import  asyncio
import json
from abc import ABC,abstractmethod
from typing import List,Callable
from rich.console import Console

import threading
import queue


class QueueService(ABCvice):
    @abstractmethod

    async def publish(self,channel:str,message:str)->None:
        pass

    async def subscribe(self,channel,callback:Callable)->None:
        pass

    

