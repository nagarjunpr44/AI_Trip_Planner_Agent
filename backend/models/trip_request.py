from pydantic import BaseModel,Field
from typing import List,Optional

class Triprequest(BaseModel):
    destination:str=Field(description="Description city or Country")
    days:int=Field(description="Number of days for the trip")
    budget:Optional[float|None]=Field(default=None,description="Total budget if provided")
    interests:List[str]=Field(default=[],description="User interests(e.g, food,adventures)")
    activities:List[str]=Field(default=[],description="User interests(e.g, food,adventures)")

class RedditURLAnalysis(BaseModel):
    selected_urls:List[str]=Field(description="List of Reddit URLs that contain valuable information for answering the user's question")



