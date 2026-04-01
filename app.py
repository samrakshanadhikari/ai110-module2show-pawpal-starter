from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def priority_to_number(priority_label: str) -> int:
    """Convert UI priority labels into numeric priority values."""
    priority_map = {"low": 1, "medium": 3, "high": 5}
    return priority_map[priority_label]


def get_owner() -> Owner:
    """Return the persisted owner object for the current session."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(
            name="Jordan",
            available_hours_per_day=2,
            preferences=[],
            location="",
        )
    return st.session_state.owner


def get_next_task_id() -> int:
    """Return the next task id and advance the session counter."""
    task_id = st.session_state.next_task_id
    st.session_state.next_task_id += 1
    return task_id


def task_rows(owner: Owner, tasks: list[Task]) -> list[dict[str, str | int]]:
    """Build table rows for task display."""
    pet_lookup = {
        task.task_id: pet.name
        for pet in owner.pets
        for task in pet.tasks
    }
    return [
        {
            "pet": pet_lookup.get(task.task_id, "Unknown"),
            "task": task.description,
            "due_date": task.due_date.isoformat(),
            "due_time": task.due_time or "Any time",
            "duration": task.duration,
            "priority": task.priority,
            "frequency": task.frequency,
            "status": task.status_label(),
        }
        for task in tasks
    ]


def incomplete_task_options(owner: Owner) -> list[tuple[str, int]]:
    """Return labels and ids for incomplete tasks."""
    options: list[tuple[str, int]] = []
    for pet in owner.pets:
        for task in pet.tasks:
            if not task.completed:
                label = (
                    f"{pet.name}: {task.description} "
                    f"({task.due_date.isoformat()} {task.due_time or 'Any time'})"
                )
                options.append((label, task.task_id))
    return options


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

owner = get_owner()
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("A polished pet-care planner powered by your Python scheduling logic.")

st.markdown(
    """
This UI now reflects the smarter backend features you built: sorted schedules,
filters, recurring tasks, and conflict warnings.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps a busy pet owner organize care tasks based on time,
priority, recurrence, and simple conflict checks.
"""
    )

st.subheader("Owner Setup")

with st.form("owner_form", clear_on_submit=False):
    owner_name = st.text_input("Owner name", value=owner.name)
    available_hours = st.number_input(
        "Available hours today",
        min_value=1,
        max_value=24,
        value=owner.available_hours_per_day,
    )
    location = st.text_input("Location", value=owner.location)
    owner_saved = st.form_submit_button("Save owner details")

if owner_saved:
    owner.name = owner_name
    owner.update_availability(int(available_hours))
    owner.location = location
    st.success("Owner details updated.")

st.caption(owner.get_today_window())

st.divider()

st.subheader("Add a Pet")

with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=1)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.error("Please enter a pet name.")
    elif any(pet.name.lower() == pet_name.strip().lower() for pet in owner.pets):
        st.warning("That pet is already in the household.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(pet_age)))
        st.success(f"Added {pet_name.strip()} to {owner.name}'s household.")

if owner.pets:
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age, "tasks": len(pet.tasks)}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets added yet. Add your first pet above.")

st.divider()

st.subheader("Add a Task")

if owner.pets:
    with st.form("task_form", clear_on_submit=True):
        task_pet_name = st.selectbox("Choose a pet", [pet.name for pet in owner.pets])
        task_description = st.text_input("Task description", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            due_date_value = st.date_input("Due date", value=date.today())
        with col2:
            due_time = st.text_input("Due time (HH:MM)", value="08:00")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        scheduler.add_task(
            task_pet_name,
            Task(
                task_id=get_next_task_id(),
                description=task_description.strip() or "Untitled task",
                duration=int(duration),
                due_time=due_time.strip() or None,
                due_date=due_date_value,
                frequency=frequency,
                priority=priority_to_number(priority_label),
            ),
        )
        st.success(f"Added task for {task_pet_name}.")
else:
    st.info("Add a pet before creating tasks.")

st.divider()

st.subheader("Task Dashboard")

pet_filter = st.selectbox(
    "Filter by pet",
    ["All pets"] + [pet.name for pet in owner.pets],
)
status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

completed_value = None
if status_filter == "Pending":
    completed_value = False
elif status_filter == "Completed":
    completed_value = True

filtered_tasks = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All pets" else pet_filter,
    completed=completed_value,
)

if filtered_tasks:
    st.table(task_rows(owner, filtered_tasks))
else:
    st.info("No tasks match the current filters.")

conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No scheduling conflicts detected right now.")

task_options = incomplete_task_options(owner)
if task_options:
    selected_task_label = st.selectbox(
        "Mark a task complete",
        [label for label, _ in task_options],
    )
    if st.button("Complete selected task"):
        selected_task_id = dict(task_options)[selected_task_label]
        next_task = scheduler.mark_task_complete(selected_task_id)
        st.success("Task marked complete.")
        if next_task is not None:
            st.info(
                f"Recurring task created for {next_task.due_date.isoformat()} "
                f"at {next_task.due_time or 'Any time'}."
            )

st.divider()

st.subheader("Today's Sorted Schedule")

if st.button("Generate schedule"):
    plan = scheduler.generate_plan()
    if plan.ordered_tasks:
        st.success("Schedule generated.")
        st.write(plan.summarize())
        st.caption(scheduler.explain_plan())
        st.table(task_rows(owner, plan.ordered_tasks))
    else:
        st.warning("Add at least one task before generating a schedule.")
