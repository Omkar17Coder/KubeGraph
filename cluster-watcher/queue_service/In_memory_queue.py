import asyncio
from abc import ABC, abstractmethod
from typing import Callable
from rich.console import Console
import threading
import queue
from base_queue import QueueService
from message_format import MonitoringMessage


class InMemoryQueueService(QueueService):
    def __init__(self):
        self.queue = {}
        self.subscribers = {}
        self.console = Console()

    async def publish(self, channel: str, message:MonitoringMessage) -> None:
        if channel not in self.queue:
            self.queue[channel] = queue.Queue()

        self.queue[channel].put(message)
        self.console.log(f"[green]Published message to {channel}[/green]")

        if channel in self.subscribers:
            tasks = [
                asyncio.create_task(callback(message))
                for callback in self.subscribers[channel]
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    callback_name = self.subscribers[channel][i].__name__
                    self.console.log(f"[red]Error in subscriber callback - {callback_name}: {result}[/red]")

    async def subscribe(self, channel: str, callback: Callable) -> None:
        if channel not in self.subscribers:
            self.subscribers[channel] = []

        self.subscribers[channel].append(callback)
        self.console.log(f"[blue]Subscribed to {channel}[/blue]")


# Global instance
queue_service = InMemoryQueueService()
