from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(owner: Owner, scheduler: Scheduler) -> None:
    """Print a readable schedule for the terminal."""
    plan = scheduler.generate_plan()

    print(f"Today's Schedule for {owner.name}")
    print("=" * 32)
    print(owner.get_today_window())
    print()

    for index, task in enumerate(plan.ordered_tasks, start=1):
        due_time = task.due_time or "Any time"
        print(
            f"{index}. {due_time} | {task.description} | "
            f"{task.duration} min | priority {task.priority} | {task.status_label()}"
        )

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
        )
    )
    mochi.add_task(
        Task(
            task_id=2,
            description="Feed breakfast",
            duration=10,
            due_time="08:30",
            priority=4,
        )
    )
    luna.add_task(
        Task(
            task_id=3,
            description="Give medication",
            duration=5,
            due_time="09:00",
            priority=5,
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    return owner, Scheduler(owner)


if __name__ == "__main__":
    demo_owner, demo_scheduler = build_demo_data()
    print_schedule(demo_owner, demo_scheduler)
