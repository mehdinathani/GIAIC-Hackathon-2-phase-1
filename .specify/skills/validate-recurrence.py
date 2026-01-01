"""
Skill: validate-recurrence
Description: Validates that task recurrence logic is working correctly by simulating completion.
"""

import sys
import os

# Add src to path to ensure todo package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from datetime import datetime
from todo.models import TaskCreate, RecurrenceEnum
from todo.service import TaskService
from todo.repository import InMemoryTaskRepository

def validate():
    print("🚀 Validating Task Recurrence Logic...")
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    # Test DAILY
    print("Testing DAILY recurrence...")
    t1 = service.create_task(TaskCreate(title="Daily", recurrence=RecurrenceEnum.DAILY))
    service.complete_task(t1.id)
    tasks = service.list_tasks()
    if len(tasks) != 2:
        print("❌ FAILED: DAILY task completion did not spawn a new task.")
        return False
    print("✅ DAILY task spawned new task.")

    # Test WEEKLY
    print("Testing WEEKLY recurrence...")
    t2 = service.create_task(TaskCreate(title="Weekly", recurrence=RecurrenceEnum.WEEKLY))
    service.complete_task(t2.id)
    tasks = service.list_tasks()
    # Should have: t1_orig, t1_new, t2_orig, t2_new
    if len(tasks) != 4:
        print(f"❌ FAILED: WEEKLY task completion did not spawn a new task. Total tasks: {len(tasks)}")
        return False
    print("✅ WEEKLY task spawned new task.")

    print("✨ All recurrence validations passed!")
    return True

if __name__ == "__main__":
    if validate():
        sys.exit(0)
    else:
        sys.exit(1)
