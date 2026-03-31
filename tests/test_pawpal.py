from pawpal_system import Pet, Task


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
