from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from typing import List, Optional


def _time_sort_key(due_time: Optional[str]) -> tuple[int, str]:
    """Return a stable key for sorting task times."""
    if not due_time:
        return (1, "99:99")
    return (0, due_time)


@dataclass
class Task:
    """Represent a single pet care activity."""

    task_id: int
    description: str
    duration: int
    due_time: Optional[str]
    frequency: str = "daily"
    priority: int = 3
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_completed(self) -> None:
        """Alias for mark_complete used by the earlier skeleton."""
        self.mark_complete()

    def reschedule(self, new_time: str) -> None:
        """Update the task due time."""
        self.due_time = new_time

    def update_details(self, **kwargs) -> None:
        """Update task fields in place."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_overdue(self, current_time: Optional[str] = None) -> bool:
        """Return True when an incomplete task is past its due time."""
        if self.completed or not self.due_time:
            return False

        today = date.today()
        if self.due_date < today:
            return True
        if self.due_date > today:
            return False

        if current_time is None:
            current_time = datetime.now().strftime("%H:%M")

        return current_time > self.due_time

    def status_label(self) -> str:
        """Return a short human-readable status label."""
        return "done" if self.completed else "pending"

    def next_due_date(self) -> Optional[date]:
        """Return the next due date for recurring tasks."""
        frequency = self.frequency.lower()
        if frequency == "daily":
            return self.due_date + timedelta(days=1)
        if frequency == "weekly":
            return self.due_date + timedelta(weeks=1)
        return None

    def spawn_next_occurrence(self, next_task_id: int) -> Optional[Task]:
        """Create the next recurring task instance when applicable."""
        next_date = self.next_due_date()
        if next_date is None:
            return None

        return replace(
            self,
            task_id=next_task_id,
            completed=False,
            due_date=next_date,
        )


@dataclass
class Pet:
    """Store pet details and related care tasks."""

    name: str
    species: str
    age: int
    preferences: List[str] = field(default_factory=list)
    dietary_requirements: List[str] = field(default_factory=list)
    medication_list: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def update_details(
        self,
        *,
        age: Optional[int] = None,
        species: Optional[str] = None,
    ) -> None:
        """Update editable pet details."""
        if age is not None:
            self.age = age
        if species is not None:
            self.species = species

    def add_preference(self, preference: str) -> None:
        """Add a care preference if it is new."""
        if preference not in self.preferences:
            self.preferences.append(preference)

    def add_task(self, task: Task) -> None:
        """Attach a new task to this pet."""
        self.tasks.append(task)

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return this pet's tasks, optionally excluding completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]

    def is_hungry(self) -> bool:
        """Return True when a pending feeding task exists."""
        return any(
            "feed" in task.description.lower() and not task.completed
            for task in self.tasks
        )

    def needs_medication_today(self) -> bool:
        """Return True when a pending medication task exists."""
        return any(
            "med" in task.description.lower() and not task.completed
            for task in self.tasks
        )


@dataclass
class Owner:
    """Represent a pet owner and their collection of pets."""

    name: str
    available_hours_per_day: int
    preferences: List[str] = field(default_factory=list)
    location: str = ""
    pets: List[Pet] = field(default_factory=list)

    def update_availability(self, hours: int) -> None:
        """Set the owner's daily available time."""
        self.available_hours_per_day = hours

    def set_preference(self, preference: str) -> None:
        """Add a preference if it is not already stored."""
        if preference not in self.preferences:
            self.preferences.append(preference)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""
        self.pets.append(pet)

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Collect tasks across every pet."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks(include_completed=include_completed))
        return all_tasks

    def get_today_window(self) -> str:
        """Return the owner's daily time budget in readable form."""
        return f"{self.available_hours_per_day} hour(s) available today"


@dataclass
class DailyPlan:
    """Represent the generated schedule for a single day."""

    date: str
    ordered_tasks: List[Task]
    total_duration: int
    completion_status: str = "pending"

    def summarize(self) -> str:
        """Return a compact summary of the plan."""
        return (
            f"{self.date}: {len(self.ordered_tasks)} task(s), "
            f"{self.total_duration} minute(s) total"
        )

    def get_next_task(self) -> Optional[Task]:
        """Return the next incomplete task in schedule order."""
        for task in self.ordered_tasks:
            if not task.completed:
                return task
        return None

    def remaining_time(self) -> int:
        """Return the remaining minutes for incomplete tasks."""
        return sum(task.duration for task in self.ordered_tasks if not task.completed)


class Scheduler:
    """Organize an owner's pet-care tasks into a daily schedule."""

    def __init__(self, owner: Owner):
        """Create a scheduler for a specific owner."""
        self.owner = owner
        self.tasks_list: List[Task] = []
        self.time_budget: int = owner.available_hours_per_day * 60
        self.constraints = {"max_minutes": self.time_budget}
        self.plan_output: Optional[DailyPlan] = None

    def refresh_tasks(self) -> List[Task]:
        """Reload tasks from the owner's pets."""
        self.tasks_list = self.owner.get_all_tasks(include_completed=False)
        return list(self.tasks_list)

    def _next_task_id(self) -> int:
        """Return the next available task id across all pets."""
        all_tasks = self.owner.get_all_tasks(include_completed=True)
        if not all_tasks:
            return 1
        return max(task.task_id for task in all_tasks) + 1

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by due date, due time, and priority."""
        tasks_to_sort = list(tasks if tasks is not None else self.refresh_tasks())
        return sorted(
            tasks_to_sort,
            key=lambda task: (task.due_date, _time_sort_key(task.due_time), -task.priority, task.task_id),
        )

    def filter_tasks(
        self,
        *,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by completion state and/or pet name."""
        filtered_tasks: List[Task] = []
        for pet in self.owner.pets:
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                filtered_tasks.append(task)
        return self.sort_by_time(filtered_tasks)

    def add_task(self, pet_name: str, task: Task) -> None:
        """Add a task to a specific pet by name."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                pet.add_task(task)
                self.refresh_tasks()
                return
        raise ValueError(f"No pet named '{pet_name}' found for owner {self.owner.name}.")

    def remove_task(self, task_id: int) -> None:
        """Remove a task from whichever pet owns it."""
        for pet in self.owner.pets:
            for task in list(pet.tasks):
                if task.task_id == task_id:
                    pet.tasks.remove(task)
                    self.refresh_tasks()
                    return
        raise ValueError(f"Task id {task_id} was not found.")

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """Complete a task and create the next recurring task when needed."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.task_id == task_id:
                    task.mark_complete()
                    next_task = task.spawn_next_occurrence(self._next_task_id())
                    if next_task is not None:
                        pet.add_task(next_task)
                    self.refresh_tasks()
                    return next_task
        raise ValueError(f"Task id {task_id} was not found.")

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for tasks that share the same scheduled time."""
        scheduled_items: List[tuple[str, Task]] = []
        for pet in self.owner.pets:
            for task in pet.get_tasks(include_completed=False):
                if task.due_time:
                    scheduled_items.append((pet.name, task))

        sorted_items = sorted(
            scheduled_items,
            key=lambda item: (item[1].due_date, item[1].due_time, item[0], item[1].task_id),
        )

        warnings: List[str] = []
        for current, nxt in zip(sorted_items, sorted_items[1:]):
            current_pet, current_task = current
            next_pet, next_task = nxt
            if (
                current_task.due_date == next_task.due_date
                and current_task.due_time == next_task.due_time
            ):
                warnings.append(
                    f"Conflict warning: {current_pet}'s '{current_task.description}' and "
                    f"{next_pet}'s '{next_task.description}' are both scheduled for "
                    f"{current_task.due_date.isoformat()} at {current_task.due_time}."
                )
        return warnings

    def apply_constraints(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Trim tasks to fit within the owner's available time."""
        tasks_to_use = list(tasks if tasks is not None else self.refresh_tasks())
        selected_tasks: List[Task] = []
        used_minutes = 0

        for task in tasks_to_use:
            if used_minutes + task.duration <= self.time_budget:
                selected_tasks.append(task)
                used_minutes += task.duration

        return selected_tasks

    def generate_plan(self) -> DailyPlan:
        """Build a time-ordered daily plan."""
        tasks = self.sort_by_time(self.refresh_tasks())
        constrained_tasks = self.apply_constraints(tasks)
        total_duration = sum(task.duration for task in constrained_tasks)
        self.plan_output = DailyPlan(
            date=date.today().isoformat(),
            ordered_tasks=constrained_tasks,
            total_duration=total_duration,
        )
        return self.plan_output

    def explain_plan(self) -> str:
        """Explain how the current plan was chosen."""
        if self.plan_output is None:
            self.generate_plan()

        assert self.plan_output is not None
        lines = [
            f"Schedule built for {self.owner.name} with {self.time_budget} available minute(s).",
            "Tasks are ordered by due date and time first, then by priority.",
        ]

        unscheduled = len(self.tasks_list) - len(self.plan_output.ordered_tasks)
        if unscheduled > 0:
            lines.append(
                f"{unscheduled} task(s) were left out because they exceeded the daily time budget."
            )

        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append(f"{len(conflicts)} conflict warning(s) detected in the task list.")

        return "\n".join(lines)
