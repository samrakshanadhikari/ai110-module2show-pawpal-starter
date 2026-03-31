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
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks_list: List[Task] = []
        self.time_budget: int = owner.available_hours_per_day * 60  # in minutes
        self.constraints: Dict = {"max_priority": 5, "min_duration": 5}  # example constraints
        self.plan_output: Dict = {}

    def add_task(self, task: Task):
        self.tasks_list.append(task)

    def remove_task(self, task_id: int):
        self.tasks_list = [t for t in self.tasks_list if t.task_id != task_id]

    def generate_plan(self) -> DailyPlan:
        # Sort tasks by priority (higher first), then by duration (shorter first for better fit)
        sorted_tasks = sorted(self.tasks_list, key=lambda t: (-t.priority, t.duration))
        selected_tasks = []
        total_time = 0
        for task in sorted_tasks:
            if total_time + task.duration <= self.time_budget:
                selected_tasks.append(task)
                total_time += task.duration
            else:
                break  # can't fit more
        from datetime import date
        today = date.today().isoformat()
        plan = DailyPlan(date=today, ordered_tasks=selected_tasks, total_duration=total_time)
        self.plan_output = {"plan": plan, "reason": f"Selected {len(selected_tasks)} tasks based on priority and time budget."}
        return plan

    def apply_constraints(self):
        # Filter tasks based on constraints, e.g., priority <= max_priority
        self.tasks_list = [t for t in self.tasks_list if t.priority <= self.constraints.get("max_priority", 5)]

    def explain_plan(self) -> str:
        return self.plan_output.get("reason", "No plan generated yet.")

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