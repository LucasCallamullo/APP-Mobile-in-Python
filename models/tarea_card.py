

from kivymd.app import MDApp
from kivy.properties import BooleanProperty
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


from models.tarea import save_wb_task_data
from models.tarea import save_ab_task_data


class TareaCard(TwoLineAvatarIconListItem):
    def __init__(self, tarea, is_open=False, **kwargs):

        """
        Parameters:
            **kwargs: Keyword arguments for initialization.
            tarea: A fully created Tarea object (i.e., it has already gone through create(cls) from tarea.py).
            is_open: Indicates whether the application is currently running (False) or starting (True).
            tarea_state: This was created to have an instance variable for use in design conditions within
            the .kv file.

        Notes:
            - The tarea_state is used to manage the state of the task for UI purposes.
            - soft_delete is used to track if the task has been marked for soft deletion.
        """

        super(TareaCard, self).__init__(**kwargs)
        self.tarea = tarea

        self.tarea_state = self.tarea.state
        self.soft_delete = self.tarea.soft_delete

        self.update_texts_on_label()

        self.dialog = None

        if not is_open:
            # Add the task to the list of all tasks from app_main.
            MDApp.get_running_app().list_tasks.append(self.tarea)

            # Save the new task to the binary file at the end.
            save_ab_task_data(task=self.tarea)

    def __str__(self):
        return "hi tarea card"

    # =================================================================
    #       Buttons Actions of Tarea Card
    # =================================================================
    def on_press(self, *args):
        """
        Notes:
            - This method is triggered when the Label containing the Task is pressed.
            - It navigates to the "info_task" screen to show detailed information about the task.
            - It also calls the `update_info_task_screen` method of the "info_task" screen to prepare
              the screen with the necessary data.

        """
        # Get the main screen from the running app
        main_screen = MDApp.get_running_app().root.get_screen("main")
        # Access the history screen from the main screen
        history_screen = main_screen.ids.history_screen

        # If the history screen is in edit mode, do nothing
        if history_screen.edit_mode:
            return

        # Get the info task screen from the app
        info_screen = MDApp.get_running_app().root.get_screen("info_task")
        # Update the info task screen with the task data
        info_screen.update_info_task_screen(self.tarea)
        # Switch to the info task screen
        MDApp.get_running_app().root.current = "info_task"

    def check_complete(self, i, value):
        """
        Args:
            i (int): The index of the checkbox. (This argument is required) ?¿
            value (bool): The state of the checkbox (True if checked, False if not).

        Notes:
            - Updates both `tarea_state` and `self.tarea.state`. These are not the same;
              `tarea_state` is the state specific to the `TareaCard`, whereas `self.tarea.state`
              refers to the state of the `Tarea` object itself.
        """
        # Update the state of the `Tarea` object based on the checkbox value
        # self.tarea.state = True if value else False
        self.tarea.state = value

        # Also update the `tarea_state` for the `TareaCard`
        self.tarea_state = self.tarea.state

        # Print the updated state for debugging purposes
        # print("The self.tarea.state is:", self.tarea.state)

    # =================================================================
    #       Updates Labels Texts.
    # =================================================================
    def update_texts_on_label(self):
        """
        Notes:
            - Updates the text and time values displayed on the label.
            - This method is responsible for setting the primary and secondary text
              of the widget based on the `Tarea` object attributes.
        """
        # Set the primary text to the task description
        self.text = self.tarea.description

        # Combine hour and minute into a formatted string and set it as the secondary text
        combined_value = f"{self.tarea.hour:02d}:{self.tarea.minute:02d}"
        self.secondary_text = combined_value

    # =================================================================
    #       REFERIDO A MD DIALOG
    # =================================================================
    def create_dialog(self, text_title="", text_label="", list_buttons=None):
        """
        Creates and displays a generic dialog with customizable buttons.

        Args:
            text_title (str): The title of the dialog.
            text_label (str): The main text of the dialog.
            list_buttons (tuple): List of labels for the buttons.
                                  If not provided, default values ("Completed", "Incomplete", "Cancel") are used.

        Notes:
            - If `list_buttons` is not provided, default button labels are used.
            - The dialog is created and opened only if it does not already exist.
            - Button actions are bound to methods for handling task state updates and dialog closure.
        """
        if list_buttons is None:
            list_buttons = ("Completed", "Incomplete", "Cancel")

        if not self.dialog:
            self.dialog = MDDialog(
                text=text_label,
                title=text_title,
                on_pre_dismiss=self.dialog_reset,
                buttons=[
                    MDFlatButton(
                        text=list_buttons[0],
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.count_tasks_one,
                    ),
                    MDFlatButton(
                        text=list_buttons[1],
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.count_tasks_zero,
                    ),
                    MDFlatButton(
                        text=list_buttons[2],
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.dialog_close,
                    ),
                ],
            )
            self.dialog.open()

    def dialog_reset(self, *args, **kwargs):
        """
        Notes:
            This call on pre_dismiss event is for reset correctly the dialog
        """
        self.dialog = None

    def dialog_close(self, *args, **kwargs):
        """
        Closes the current dialog and removes it.

        Notes:
            - The dialog is dismissed and the reference to it is set to None.
        """
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = None

    def count_tasks_one(self, *args, **kwargs):
        """
        Marks the task as completed, saves it in the task list, and closes the dialog.

        Notes:
            - Appends a value of 1 to the `list_repeat` attribute of the task.
            - Updates the task in the main application’s task list.
            - Calls `dialog_close` to close the dialog.
            - Saves the updated task data.
        """
        self.tarea.list_repeat.append(1)

        # Updates the task list in the main application.
        MDApp.get_running_app().list_tasks[self.tarea.id] = self.tarea

        # Print to check if the task is saved correctly
        # print(self.tarea)

        self.dialog_close()

        # Save the updated task data. Tarea Module
        save_wb_task_data()

    def count_tasks_zero(self, *args, **kwargs):
        """
        Marks the task as incomplete, saves it in the task list, and closes the dialog.

        Notes:
            - Appends a value of 0 to the `list_repeat` attribute of the task to indicate incompleteness.
            - Updates the task in the main application’s task list.
            - Calls `dialog_close` to close the dialog.
            - Saves the updated task data.
        """
        self.tarea.list_repeat.append(0)

        # Updates the task list in the main application.
        MDApp.get_running_app().list_tasks[self.tarea.id] = self.tarea

        self.dialog_close()

        # Save the updated task data.
        save_wb_task_data()


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        """
        Initializes the RightCheckbox.

        Notes:
            - Used in the creation of the Task Card to determine whether a task has been completed or not.
            - It has its own `active` attribute, which is simply a boolean.
        """
        super(RightCheckbox, self).__init__(**kwargs)