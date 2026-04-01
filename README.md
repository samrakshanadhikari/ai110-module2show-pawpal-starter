# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Features

- Manage an owner profile with a daily time budget
- Add multiple pets and store tasks for each pet
- Sort schedules by due date and time
- Filter tasks by pet and completion status
- Auto-create the next daily or weekly task when a recurring task is completed
- Detect exact-time conflicts and show warning messages instead of crashing
- Generate a daily plan that fits within the owner's available time

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ now includes a few lightweight scheduling algorithms to make plans more useful:

- Sort tasks by due date and time so schedules print in a natural order
- Filter tasks by pet name or completion status
- Auto-create the next instance of daily and weekly recurring tasks when one is completed
- Detect exact-time task conflicts and return warning messages instead of failing

## 📸 Demo

The UI now exposes sorted task views, task filters, recurring task completion, and conflict warnings.

I could not capture a real browser screenshot from this terminal-only environment, so this section is ready for your final local screenshot export before submission. After you take the image locally, replace `your_screenshot_name.png` in the embed below.

```html
<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>
```

## Architecture

- Final UML diagram: [`uml_final.svg`](uml_final.svg)
- Core backend logic: [`pawpal_system.py`](pawpal_system.py)
- Streamlit UI: [`app.py`](app.py)

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

The tests cover task completion, adding tasks to pets, chronological sorting, filtering by pet and status, recurring daily tasks, empty schedules, and exact-time conflict detection.

Confidence Level: 4/5 stars. The current suite gives strong coverage for the core scheduling behaviors, but there is still room to add more edge-case testing for invalid inputs, overlapping durations, and Streamlit UI workflows.
