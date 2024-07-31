
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

# Importa solo las clases necesarias
from models.day_button import GridButtonsDay
from models.popup_time_select import PopupSelectTime

from models.tarea import Tarea
from models.tarea_card import TareaCard

from models.snackbar_generic import *


class AddTaskScreen(MDScreen):

    def __init__(self, **kwargs):
        """
        Constructor for the AddTaskScreen class.

        Notes:
            - `popup` creates the PopupSelectTime as an object within the screen to call it when needed.
            - `description` (str): Refers to the text value entered. Starts empty as a flag.
            - `hours_value` (int): The hour retrieved from the popup, starts at -1 as a flag.
        """
        super(AddTaskScreen, self).__init__(**kwargs)
        self.popup = PopupSelectTime()

        self.description = ""
        self.hours_value = -1
        self.minutes_value = 0

        self.tarea = None
        self.id_text_snackbar = ""

    # =================================================================
    #       Updates Labels Texts.
    # =================================================================
    def reset_grid_buttons(self):
        """
        Notes: This is called every time the tab screen is exited to reset the button values
        """
        self.ids.grid_buttons.reset_days_buttons()

    def reset_text_labels_n_icon(self, text_task="", text_time="", icon="note-alert-outline"):
        self.ids.display_work.text = text_task
        self.ids.display_time.text = text_time
        self.ids.input_field.text = ""
        self.ids.input_field.icon_right = icon

    def update_label_text(self, description):
        """
        Updates the MDLabel displaying the task with the new text entered.

        Args:
            description (str): The new description to be displayed.

        Notes:
            - The `self.description` attribute is updated with the provided description,
              which is stripped of leading and trailing whitespace and capitalized.
            - The updated description is then appended to the text of `self.ids.display_work`.
        """
        self.description = description.strip().capitalize()
        self.ids.display_work.text += f"{self.description}"

    def update_label_hour(self, hours_value, minutes_value):
        self.hours_value = int(hours_value)
        self.minutes_value = int(minutes_value)
        self.ids.display_time.text += f"{self.hours_value:02d}:{self.minutes_value:02d}"

    # =================================================================
    #       Buttons Actions of Task Screen
    # =================================================================
    def add_todo(self):
        """
        Notes:
            - This method is called from (work_screen: button_aceptar) and it calls Tarea.create() to create a new task
              based on the data filled in the various labels of add_work.
            - If the task is created successfully, it returns a Tarea object; otherwise, it returns None.
            - If a task is created, it adds a TodoCard() widget to the (main_screen: id:todo_list).

        =======================================================================================================
            Although this method works, it might be problematic if you want to reset the data when leaving add_work.
            Consider creating a Tarea class instance in work_screen as an attribute and passing it as an argument.
        =======================================================================================================
        """
        list_days = self.ids.grid_buttons.list_active_day_button()

        # Additionally, it returns the id_text to display in the SnackBar in case of creation failure.
        self.tarea, self.id_text_snackbar = Tarea.create(
                        list_days=list_days, desc=self.description,
                        hour=self.hours_value, minute=self.minutes_value)

        if self.tarea:
            # Create the TareaCard object to add to the todo_list through a method of main_screen
            task_to_add = TareaCard(self.tarea)
            task_to_add2 = TareaCard(self.tarea, True)
            task_to_add3 = TareaCard(self.tarea, True)

            main_screen = MDApp.get_running_app().root.get_screen("main")

            main_screen.ids.todo_list.add_widget_in_todo_list(task_to_add)

            history_screen = main_screen.ids.history_screen
            history_screen.ids.selection_list.add_widget_in_todo_list(task_to_add2)
            # history_screen.listar_callback()

            all_tasks_screen = MDApp.get_running_app().root.get_screen("all_tasks_screen")
            all_tasks_screen.ids.selection_all_list.add_widget_in_todo_list(task_to_add3)

    def switch_navigation(self):
        """
        Notes:
            - Simply switches to the "main_tab" directly, as you cannot navigate directly to the "main" screen
              due to the bottom_navigation.
        """
        main_screen = MDApp.get_running_app().root.get_screen("main")
        main_screen.ids.bottom_nav.switch_tab("main_tab")
