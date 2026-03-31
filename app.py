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


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

owner = get_owner()

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This version connects the Streamlit interface to your Python classes so pets and tasks
persist in session memory while you use the app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
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
    st.write("Current pets:")
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
        due_time = st.text_input("Due time (HH:MM)", value="08:00")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        scheduler = Scheduler(owner)
        scheduler.add_task(
            task_pet_name,
            Task(
                task_id=get_next_task_id(),
                description=task_description.strip() or "Untitled task",
                duration=int(duration),
                due_time=due_time.strip() or None,
                frequency=frequency,
                priority=priority_to_number(priority_label),
            ),
        )
        st.success(f"Added task for {task_pet_name}.")
else:
    st.info("Add a pet before creating tasks.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": task.description,
                "due_time": task.due_time or "Any time",
                "duration": task.duration,
                "priority": task.priority,
                "status": task.status_label(),
            }
            for pet in owner.pets
            for task in pet.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    if plan.ordered_tasks:
        st.success("Schedule generated.")
        st.write(plan.summarize())
        st.write(scheduler.explain_plan())
        st.table(
            [
                {
                    "task": task.description,
                    "due_time": task.due_time or "Any time",
                    "duration": f"{task.duration} min",
                    "priority": task.priority,
                }
                for task in plan.ordered_tasks
            ]
        )
    else:
        st.warning("Add at least one task before generating a schedule.")
