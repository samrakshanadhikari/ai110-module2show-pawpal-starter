# PawPal+ Project Reflection

## 1. System Design

### 1d. Building Blocks (main objects)

- Pet
  - Attributes: name, species, age, preferences, dietary requirements, medication list
  - Methods: update_details(), add_preference(), is_hungry(), needs_medication_today()

- Owner
  - Attributes: name, available_hours_per_day, preferences, location
  - Methods: update_availability(), set_preference(), get_today_window()

- Task
  - Attributes: task_id, type (walk/feed/med/enrichment/groom), duration, priority, due_time, notes, completed
  - Methods: mark_completed(), reschedule(), update_details(), is_overdue()

- Scheduler (or Planner)
  - Attributes: tasks_list, time_budget, constraints, plan_output
  - Methods: add_task(), remove_task(), generate_plan(), apply_constraints(), explain_plan()

- DailyPlan (optional)
  - Attributes: date, ordered_tasks, total_duration, completion_status
  - Methods: summarize(), get_next_task(), remaining_time()

**a. Initial design**

The initial UML design uses a class diagram to model the PawPal+ system with five main classes: Owner, Pet, Task, Scheduler, and DailyPlan. The Owner class represents the pet owner and manages their availability and preferences. The Pet class holds information about the pet's details and needs. The Task class defines individual care tasks with attributes like type, duration, and priority. The Scheduler class handles the logic for generating daily plans based on tasks and constraints. The DailyPlan class represents the output schedule for a day. Relationships include Owner having Pets, Scheduler managing Tasks and generating DailyPlans, and DailyPlans containing Tasks.

What classes did you include, and what responsibilities did you assign to each?

- **Owner**: Manages owner information and preferences; provides methods for updating availability and getting time windows.
- **Pet**: Stores pet details and needs; includes methods for updating info and checking status like hunger or medication needs.
- **Task**: Represents care tasks; handles completion, rescheduling, and status checks.
- **Scheduler**: Core logic for planning; adds/removes tasks, generates plans, applies constraints, and explains decisions.
- **DailyPlan**: Output of the scheduler; summarizes the day's tasks and tracks progress.

**b. Design changes**

No design changes were made during this initial implementation phase. The skeleton classes were created directly from the UML diagram without modifications, as the AI review confirmed the structure was appropriate and complete for the current requirements.

**c. Core actions**

- **Track Pet Care Tasks**: The app should allow users to track various pet care tasks such as walks, feeding, medication, enrichment activities, and grooming. This feature will help pet owners stay organized and ensure that all necessary tasks are completed on time.
- **Consider Constraints**: The app should take into account the user's available time, task priority, and personal preferences when suggesting a daily care plan. This ensures that the recommendations are tailored to the user's specific situation.
- **Produce a Daily Plan**: The app should generate a daily plan for pet care tasks and provide explanations for the chosen tasks. This feature will help users understand the reasoning behind the recommendations and improve their adherence to the care schedule.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers time constraints (owner's available hours per day, converted to minutes), task priority (1-5, higher is more important), and basic constraints like maximum priority allowed. It prioritizes time feasibility first, then sorts tasks by priority descending to ensure critical tasks (e.g., medication) are included before optional ones (e.g., grooming). I decided time mattered most because without fitting into the day, the plan is unusable; priority ensures essential care isn't skipped.

**b. Tradeoffs**

The scheduler prioritizes high-priority tasks, potentially excluding lower-priority ones that could fit into remaining time. This tradeoff is reasonable for pet care because critical tasks (like feeding or meds) must be done daily for health, while optional activities can be deferred without immediate harm.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
