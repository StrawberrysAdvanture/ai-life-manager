from enum import StrEnum


class Permission(StrEnum):
    # Task
    READ_TASKS = "read_tasks"
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"

    # Projects
    READ_PROJECTS = "read_projects"
    CREATE_PROJECT = "create_project"

    # Person
    READ_PEOPLE = "read_people"
    CREATE_PERSON = "create_person"
