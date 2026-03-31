from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Pet:
    name: str
    species: str
    age: int
    preferences: List[str]
    dietary_requirements: List[str]
    medication_list: List[str]

    def update_details(self):
        pass

    def add_preference(self, preference: str):
        pass

    def is_hungry(self) -> bool:
        pass

    def needs_medication_today(self) -> bool:
        pass

@dataclass
class Owner:
    name: str
    available_hours_per_day: int
    preferences: List[str]
    location: str

    def update_availability(self, hours: int):
        pass

    def set_preference(self, preference: str):
        pass

    def get_today_window(self) -> str:
        pass

@dataclass
class Task:
    task_id: int
    type: str  # walk/feed/med/enrichment/groom
    duration: int  # in minutes
    priority: int  # 1-5
    due_time: Optional[str]  # e.g., "10:00"
    notes: str
    completed: bool = False

    def mark_completed(self):
        pass

    def reschedule(self, new_time: str):
        pass

    def update_details(self, **kwargs):
        pass

    def is_overdue(self) -> bool:
        pass

class Scheduler:
    def __init__(self):
        self.tasks_list: List[Task] = []
        self.time_budget: int = 0
        self.constraints: Dict = {}
        self.plan_output: Dict = {}

    def add_task(self, task: Task):
        pass

    def remove_task(self, task_id: int):
        pass

    def generate_plan(self) -> 'DailyPlan':
        pass

    def apply_constraints(self):
        pass

    def explain_plan(self) -> str:
        pass

@dataclass
class DailyPlan:
    date: str
    ordered_tasks: List[Task]
    total_duration: int
    completion_status: str = "pending"

    def summarize(self) -> str:
        pass

    def get_next_task(self) -> Optional[Task]:
        pass

    def remaining_time(self) -> int:
        pass