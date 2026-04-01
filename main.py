from pawpal_system import Owner, Pet, Scheduler, Task


def print_task_list(title: str, tasks: list[Task]) -> None:
    """Print a readable task list for the terminal."""
    print(title)
    print("-" * len(title))
    for task in tasks:
        due_time = task.due_time or "Any time"
        print(
            f"{task.due_date.isoformat()} {due_time} | {task.description} | "
            f"{task.duration} min | priority {task.priority} | {task.status_label()}"
        )
    print()


def print_schedule(owner: Owner, scheduler: Scheduler) -> None:
    """Print a readable schedule and algorithm checks for the terminal."""
    plan = scheduler.generate_plan()
    conflicts = scheduler.detect_conflicts()

    print(f"Today's Schedule for {owner.name}")
    print("=" * 32)
    print(owner.get_today_window())
    print()

    print_task_list("Sorted schedule", plan.ordered_tasks)

    print("Conflict detection")
    print("------------------")
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")
    print()

    print_task_list("Mochi only", scheduler.filter_tasks(pet_name="Mochi", completed=False))

    next_task = scheduler.mark_task_complete(2)
    print("Recurring task demo")
    print("-------------------")
    print("Marked task 2 complete.")
    if next_task:
        print(
            f"Created next occurrence: {next_task.description} on "
            f"{next_task.due_date.isoformat()} at {next_task.due_time}"
        )
    else:
        print("No recurring task was created.")
    print()

    print(plan.summarize())
    print(scheduler.explain_plan())


def build_demo_data() -> tuple[Owner, Scheduler]:
    """Create sample pets and tasks for a CLI demo."""
    owner = Owner(
        name="Jordan",
        available_hours_per_day=2,
        preferences=["short morning tasks", "prioritize medication"],
        location="Chicago",
    )

    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=7)

    mochi.add_task(
        Task(
            task_id=1,
            description="Morning walk",
            duration=30,
            due_time="08:00",
            priority=5,
            frequency="daily",
        )
    )
    mochi.add_task(
        Task(
            task_id=2,
            description="Feed breakfast",
            duration=10,
            due_time="08:30",
            priority=4,
            frequency="daily",
        )
    )
    mochi.add_task(
        Task(
            task_id=3,
            description="Brush coat",
            duration=15,
            due_time="07:30",
            priority=2,
            frequency="weekly",
        )
    )
    luna.add_task(
        Task(
            task_id=4,
            description="Give medication",
            duration=5,
            due_time="09:00",
            priority=5,
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            task_id=5,
            description="Feed breakfast",
            duration=10,
            due_time="08:30",
            priority=4,
            frequency="daily",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    return owner, Scheduler(owner)


if __name__ == "__main__":
    demo_owner, demo_scheduler = build_demo_data()
    print_schedule(demo_owner, demo_scheduler)
