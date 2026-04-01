from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    """Task completion should flip the completed flag."""
    task = Task(
        task_id=1,
        description="Morning walk",
        duration=20,
        due_time="08:00",
    )

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    """Adding a task should increase the pet task list size."""
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(
        task_id=2,
        description="Feed dinner",
        duration=10,
        due_time="18:00",
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_mark_task_complete_creates_next_daily_occurrence() -> None:
    """Completing a daily task should create the next occurrence."""
    pet = Pet(name="Mochi", species="dog", age=3)
    owner = Owner(name="Jordan", available_hours_per_day=2, pets=[pet])
    task = Task(
        task_id=1,
        description="Morning walk",
        duration=20,
        due_time="08:00",
        frequency="daily",
        due_date=date.today(),
    )
    pet.add_task(task)
    scheduler = Scheduler(owner)

    next_task = scheduler.mark_task_complete(1)

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_detect_conflicts_returns_warning_for_exact_time_match() -> None:
    """Tasks at the same time should produce a conflict warning."""
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner = Owner(name="Jordan", available_hours_per_day=2, pets=[mochi, luna])

    mochi.add_task(Task(task_id=1, description="Walk", duration=20, due_time="08:00"))
    luna.add_task(Task(task_id=2, description="Feed", duration=10, due_time="08:00"))
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Conflict warning" in warnings[0]


def test_sort_by_time_returns_tasks_in_chronological_order() -> None:
    """Tasks should be sorted by date and time."""
    pet = Pet(name="Mochi", species="dog", age=3)
    owner = Owner(name="Jordan", available_hours_per_day=2, pets=[pet])

    pet.add_task(
        Task(
            task_id=1,
            description="Late walk",
            duration=20,
            due_time="09:00",
            due_date=date.today(),
        )
    )
    pet.add_task(
        Task(
            task_id=2,
            description="Early feed",
            duration=10,
            due_time="07:30",
            due_date=date.today(),
        )
    )
    pet.add_task(
        Task(
            task_id=3,
            description="Tomorrow meds",
            duration=5,
            due_time="08:00",
            due_date=date.today() + timedelta(days=1),
        )
    )
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()

    assert [task.task_id for task in sorted_tasks] == [2, 1, 3]


def test_filter_tasks_can_return_only_completed_tasks_for_one_pet() -> None:
    """Filtering should support completion state and pet name together."""
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner = Owner(name="Jordan", available_hours_per_day=2, pets=[mochi, luna])

    completed_task = Task(task_id=1, description="Walk", duration=20, due_time="08:00")
    completed_task.mark_complete()
    mochi.add_task(completed_task)
    mochi.add_task(Task(task_id=2, description="Feed", duration=10, due_time="09:00"))
    luna.add_task(Task(task_id=3, description="Brush", duration=10, due_time="10:00"))
    scheduler = Scheduler(owner)

    filtered_tasks = scheduler.filter_tasks(completed=True, pet_name="Mochi")

    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].description == "Walk"


def test_generate_plan_for_pet_with_no_tasks_returns_empty_plan() -> None:
    """A pet with no tasks should produce an empty but valid plan."""
    pet = Pet(name="Mochi", species="dog", age=3)
    owner = Owner(name="Jordan", available_hours_per_day=2, pets=[pet])
    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert plan.ordered_tasks == []
    assert plan.total_duration == 0


def test_detect_conflicts_returns_no_warnings_for_unique_times() -> None:
    """Unique task times should not produce conflict warnings."""
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner = Owner(name="Jordan", available_hours_per_day=2, pets=[mochi, luna])

    mochi.add_task(Task(task_id=1, description="Walk", duration=20, due_time="08:00"))
    luna.add_task(Task(task_id=2, description="Feed", duration=10, due_time="08:30"))
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()

    assert warnings == []
