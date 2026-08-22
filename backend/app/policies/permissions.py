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

    # Commitment
    READ_COMMITMENTS = "read_commitments"
    CREATE_COMMITMENT = "create_commitment"

    # Agent Action... only read permited here anyway
    READ_AGENT_ACTIONS = "read_agent_actions"
