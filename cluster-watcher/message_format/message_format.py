
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict,Optional,Any
import json

@dataclass

class MonitoringMessage:
    cluster_name:str
    resource_type:str
    resource_name:str
    namespace:Optional[str]
    action:str ## Created Modified Deleted.
    timestamp:datetime
    data:Dict[str,Any]
    previous_Data:Optional[Dict[str,Any]]=None



    def to_json(self)->str:
        data=asdict(self)
        data['timestamp']:self.timestamp.isoformat()
        return json.dumps(data)

    @classmethod

    def from_json(cls,json_str:str)->'MonitoringMessage':
        data=json.loads(json_str)
        data['timestamp']=datetime.fromisoformat(data['timestamp'])
        return cls(**data)
        

