# Building Scheduler

This was a recent code challenge I took part in to build a simple scheduling
system in a relatively tight 3 hour timeline.

There are improvements that should be made, but this is intended to showcase
the output of a quick coding challenge instead of being a perfect museum piece.
Some of these were captured during the challenge timeline in this document under
the `Further Work` section, some others noticed during code review.

See [REQUIREMENTS.md](REQUIREMENTS.md) for the product requirements.

## Installing/Running

- Requires Python >3.8, developed in Python 3.10
- *Should* be installed in a python virualenv, but system python will run app.py just fine

```bash
python3 app.py
```

Install in a virtualenv to run tests.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
python3 pytest
```

### Making your own schedules

- Buildings and employees are demonstrated in the tests and app.py
- Provide the employee days off as an optional third parameter `Employee(ROLE, NAME, ["Monday", "Thursday"]`
- Building types are open for extension by creating new class with appropriate requirements

### Expected Output

Hopefully you get successful tests and a final schedule from app.py

```bash
:% python3 -m pytest
======= test session starts =======
platform linux -- Python 3.10.12, pytest-7.4.2, pluggy-1.3.0
collected 34 items

./tests/test_employee.py ....              [ 11%]
./tests/test_roster.py ................    [ 58%]
./tests/test_scheduling_daily.py ......... [ 85%]
./tests/test_scheduling_weekly.py .....    [100%]

======= 34 passed in 0.05s =======
```

```bash
******** Prettier, slightly out of order output ********
{   'Friday': [   Commercial Building: Certified Charli, Certified Charles, Apprentice Agnes, Apprentice Arnold, Labourer Liam, Labourer Lindsay, Certified Chester, Certified Chelly],
    'Monday': [   Two Storey Home: Certified Charli, Apprentice Agnes,
                  Single Storey Home: Certified Charles,
                  Single Storey Home: Certified Chester,
                  Single Storey Home: Certified Chelly],
    'Thursday': [   Commercial Building: Certified Charli, Certified Charles, Apprentice Agnes, Apprentice Arnold, Labourer Liam, Labourer Lindsay, Certified Chester, Certified Chelly],
    'Tuesday': [   Commercial Building: Certified Charli, Certified Charles, Apprentice Agnes, Apprentice Arnold, Labourer Liam, Labourer Lindsay, Certified Chester, Certified Chelly],
    'Wednesday': [   Commercial Building: Certified Charli, Certified Charles, Apprentice Agnes, Apprentice Arnold, Labourer Liam, Labourer Lindsay, Certified Chester, Certified Chelly]}
Remaining Buildings
[Two Storey Home]
```

## Entities and Responsibilities

- Building
  - size/type of building places demands on pool of workers
- Employee
  - Name for clean UI scheduling
  - Role
  - Employee days off
- Employee Roster
  - Tracking which employees on the roster are available/scheduled/on leave
  - A list/container plus business logic
- Daily building schedule
  - Maps day of week->buildings->employees
- Scheduler for a whole week
  - Maps days of week -> daily schedules
- Overarching application to interact with the scheduler

## Assumptions/MVP compromises

- Iterating through each day->building->employee should allow us to fill days with fully-staffed buildings, but this assumption might bite me later
- Working from lowest to highest level components meant that I needed my base assumptions about scheduling employees to be correct when it came time to integrate them.  With a more complex, less intuitive problem I think it would be preferable to start with a simpler low-level entity and work from a middle layer?  E.g. If I were asked to calculate chess ELO for a league I would want to worry about the ELO algorithm after the roster of players because ELO is not something I am familiar with.
- Focused heavily on a single week of work.  Buildings can be left over, and are easily viewable to the user so I think this is fine for an MVP
- There might be too many tests.  I chose to go full-TDD because it was much easier for me to do that instead of trying to hold algorithmic details for a domain I'm not currently deep inside of.
- Using string names for days because it's cleaner to illustrate the point in tests.  Possibly better as numeric day indicies, or maybe `(week number, day number)` pair?
  - A customer would probably need to schedule workers on the weekend at least some time and that should not cause any issues.  Okay for MVP, and convenient when I was writing app.py to display to the user
- Python type annotations are helpful even on a tight timeline.  There were 5+ instances of reading method signatures reminding me of what I needed.  Reduced cognitive load

## Challenges

- Two scary refactors when close to the time limit:
  - Had a couple of misleading tests that I caught while filling in the top-level `schedule()` method.  Employees were being counted as scheduled but were not being added to the `DailyBuildingSchedule` so their names were not being printed out.  Business logic was intact, user output was compromised, but it was an easy fix
  - Had to make a quick switch from using `set`s to using plain lists when I was integrating daily schedules in to the weekly schedule process.  Non-deterministic ordering of `set`s makes them a bad option for the implicit-prioritization of the buildings list.  I started with a Buildings `set` to get the difference between all buildings and already-scheduled, but ordering became a higher priority.  Test coverage saved me!

## Further work

- (3/10) Replace `EmployeeRole.ANY` responsibility with hard-coded tuples: adding a 4th type of employee COULD have unintended consequences, as ANY would automatically include any new roles
- (2/10) Time-dimension improvement: `Roster.get_available_employees()` iterates through all employees every call, this will certainly lead to poor performance for large sets of employees.  Should track and mutate a list of available employees instead of using set subtraction
- (1/10) Fix the out of order printing from pprint in app.py.  Ordering is normal when calling `print()` but pprint is doing something weird.
- (1/10) Make sure python type annotations are actually correct.  They aren't actually necessary to get the tests to pass, so it's possible that I missed a couple during those last couple of refactors
- (4/10) An abstraction for `EmployeeRequirement(role)` or `WorkerSlot(role)` could be split out to improve the process of selecting employees.  The 3-stanza if-statement in `Roster.meets_worker_requirements` is awkward and could be improved
  - e.g. `WokerRequirement(Or(ANY, CERTIFIED))` is reminiscent of ORM behaviour, could also have made it more pythonic and overloaded the `__or__` method so we could say `WorkerSlot(ANY or CERTIFIED)`, though this feels a bit too clever to me and I would probably keep things simple
- (3/10) `Roster.meets_worker_requirements` needs to be cleaned up
  - Hard-coded list of supported roles was an MVP compromise when I needed to start tracking which employees of a given role were remaining
- (1/10) Using an exception `NoEmployeeAvailable` in flow control is not ideal, but it was a part of the rough-out work so I kept it.  Covered by tests and could easily be swapped out for a better structure
- (1/10) Cleaning up the story told by testing names. Ordering of tests was in the order I was working in.
- (1/10) Adding tests for app.py.  I TDD'd my way from lowest level to highest (employees -> roster -> building scheduler -> app.py) and just didn't have time to test around that
- (1/10) Personal preference about verbose employee names in tests.  Totally unnecessary, but I got in the habit of naming the employees for each test early when I was initially testing for employee names.  It looks like a lot of text, but it's mostly copy/paste or swapping a name out.  The principle at play here is to use different testing values in different scenarios so you aren't implying that there is any magic value for "Test Employee 1", though this is one of those pieces of advice I've been using for so long I forget who told me it was a good idea.
- (0/10) `EmployeeRole` class is too verbose, could be shortened to `Role`
