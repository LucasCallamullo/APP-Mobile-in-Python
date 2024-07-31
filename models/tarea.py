

import pickle
from kivymd.app import MDApp


class Tarea:
    def __init__(self, description="", hour=0, minute=0, state=False, id=-1,
                 list_days=None, list_repeat=None, soft_delete=False):
        """
        Notes:
            Constructor for the Tarea class, representing a task object.
            Each attribute serves a specific purpose:
            - description: A textual description of the task.
            - hour: The hour at which the task is scheduled.
            - minute: The minute at which the task is scheduled.
            - state: Indicates whether the task has been completed. This attribute is related to `list_repeat`.
            - id: A unique identifier for the task.
            - list_days: A list indicating the task's activity status for each day of the week.
                Initially set to [False] * 7, where each index corresponds to a day of the week,
                starting from Monday to Sunday.
            - list_repeat: A list tracking the number of times the task has been completed or missed.
                Defaults to [0] if not provided.
            - soft_delete: A boolean flag indicating if the task has been soft-deleted.
                It is initially set to False and is used to mark tasks as deleted without removing them completely.
        """
        self.description = description
        self.hour = hour
        self.minute = minute
        self.state = state
        self.id = id
        self.list_days = [False] * 7 if list_days is None else list_days
        self.list_repeat = [0] if list_repeat is None else list_repeat
        self.soft_delete = soft_delete

    def __str__(self):
        """
        Returns a string representation of the Tarea object.

        Notes:
            - This method provides a formatted string that displays the attributes of the Tarea instance.
            - It can be useful for debugging and logging to verify the stored data.
            - You may choose to remove this method if you no longer need to print the object's
            details in this format.

        :return: A string with the task's description, ID, state, hour, minute, list of active days,
                 list of repetitions, and soft delete status.
        """
        cad = f"Description: {self.description}"
        cad += f"\nID: {self.id}"
        cad += f"\nState: {self.state}"
        cad += f"\nHour: {self.hour}"
        cad += f"\nMinutes: {self.minute}"
        cad += f"\nList of Days: {self.list_days}"
        cad += f"\nList of Repeats: {self.list_repeat}"
        cad += f"\nSoft Delete: {self.soft_delete}"
        cad += "\n=========================="
        return cad

    @classmethod
    def create(cls, list_days=None, desc="", hour=-1, minute=-1, edit_mode=False, tarea_obj=None):
        """
        Creates a new instance of the `Tarea` class.

        Parameters:
        ----------
        cls: class
            Reference to the `Tarea` class.
        list_days: list of bool, optional
            List of days on which the task repeats. Defaults to None.
        desc: str, optional
            Description of the task. Defaults to an empty string.
        hour: int, optional
            Hour at which the task is to be performed. Defaults to -1.
        min: int, optional
            Minute at which the task is to be performed. Defaults to -1.
        edit_mode: bool, optional
            Indicates if the task is being edited. Defaults to False.
        tarea_obj: Tarea, optional
            Existing `Tarea` object being edited. Defaults to None.

        Returns:
        -------
        Tarea or None
            Returns a new `Tarea` instance if the conditions are met, otherwise returns None.
        int
            An integer code indicating the result:
            - 0: Description is empty.
            - 1: Hour is not specified.
            - 2: Task with the same description already exists.
            - 3: Successfully created or updated task.

        Notes:
        -----
        - In non-edit mode (`edit_mode=False`):
          - If the description is empty or the hour is not specified, prints a message and returns None.
          - If a task with the same description already exists, prints a message and returns None.
          - Assigns a new ID based on the length of the list of tasks.

        - In edit mode (`edit_mode=True`):
          - Updates the existing `tarea_obj` with the provided values, or retains the original values
          if no new values are provided.

        Example:
        -------
        # Create a new task
        new_task = Tarea.create(list_days=[True, False, True, False, True, False, True], desc="Buy milk", hour=10, min=30)

        # Edit an existing task
        edited_task = Tarea.create(edit_mode=True, tarea_obj=existing_task, desc="Check email")
        """

        if not edit_mode:
            if desc == "":
                return None, 0

            if hour == -1:
                return None, 1

            list_tasks = MDApp.get_running_app().list_tasks
            if any(tarea.description == desc for tarea in list_tasks):
                return None, 2

            # There would be no issue with the ID because the first time it would be 0, then 1,
            # and so on incrementing.
            id = len(list_tasks)
            list_days = list_days if list_days is not None else [False] * 7

            return cls(description=desc, hour=hour, minute=minute, id=id, list_days=list_days), 3

        if edit_mode:
            desc = desc if desc != "" else tarea_obj.description
            hour = hour if hour != -1 else tarea_obj.hour
            minute = minute if minute != -1 else tarea_obj.minute
            id = tarea_obj.id
            list_days = list_days if list_days is not None else [False] * 7

            return cls(description=desc, hour=hour, minute=minute, id=id, list_days=list_days)


# =================================================================
#               SAVE AND LOAD DATA FROM LISTS
# =================================================================
def save_ab_task_data(task=None, fd='tareas.dat'):
    """
    Notes:
        - This function is called every time we add a new complete task. We use "ab" mode
          to avoid rewriting the entire file and to simply append the new item to the end of the file.
        - This approach also maintains the order of the IDs.

    :param task: The task object to be appended to the file.
    :param fd: The filename of the binary file where the task will be saved. Default is 'tareas.dat'.
    """
    with open(fd, 'ab') as file:
        pickle.dump(task, file)
        file.flush()
        # print(task)


def save_wb_task_data(fd='tareas.dat'):
    """
    Notes:
        - This function is called when we confirm with the CheckBox that a Task is completed.
        - Currently, it rewrites the entire binary file with updated data.
        - Consider implementing a way to check the state only once and prevent further modifications.

    Parameters:
    ----------
    fd: str, optional
        The filename to save the data to. Default is 'tareas.dat'.
    """
    list_tasks = MDApp.get_running_app().list_tasks

    # Rewrite the binary file completely with updated data.
    with open(fd, 'wb') as file:
        for task in list_tasks:
            pickle.dump(task, file)
            file.flush()


def load_rb_task_data(fd='tareas.dat'):
    """
    Load task data from a binary file serialized with pickle.

    Parameters:
        fd (str): The name of the file to load data from. Default is 'tareas.dat'.

    Returns:
        list: A list containing all the loaded Task objects.

    Raises:
        FileNotFoundError: If the specified file (`fd`) does not exist in the system, prints an error message.
        and return a empty list

    Notes:
        This function reads binary objects from a file using pickle and uses an "EOFError" to determine the end
        of the file, without needing a .tell() method call.
    """
    list_tasks = []
    try:
        with open(fd, 'rb') as file:
            while True:
                try:
                    task_recovery = pickle.load(file)
                    list_tasks.append(task_recovery)
                    # print(task_recovery)
                except EOFError:
                    break

        return list_tasks

    except FileNotFoundError:
        print(f"The file {fd} does not exist.")
        return list_tasks
