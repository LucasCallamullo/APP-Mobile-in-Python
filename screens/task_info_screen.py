

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from kivy.properties import BooleanProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from models.day_button import GridButtonsDay
from models.popup_time_select import PopupSelectTime
from models.popup_edit_task import PopupEditWork

from models.tarea import Tarea
from models.tarea_card import TareaCard
from models.tarea import save_wb_task_data


class InfoWorkScreen(MDScreen):
    """
    Info Task screen.
    This screen is called whenever a TaskCard is touched from any screen.
    """
    # Flags to determine if we are in edit mode to edit the task
    # and to know if we have made changes or not
    edit_mode = BooleanProperty(False)
    apply_changes = BooleanProperty(False)

    def __init__(self, **kwargs):
        """
        Constructor for the InfoWorkScreen class.

        Parameters:
        ----------
        kwargs : dict
            Keyword arguments for initialization.
        """
        super(InfoWorkScreen, self).__init__(**kwargs)

        self.tarea = None  # Task object associated with this screen

        self.list_days = [False] * 7  # List of booleans indicating the active days of the week
        self.hour = -1          # Hour of the task, initialized to -1 as a flag
        self.minute = -1        # Minute of the task, initialized to -1 as a flag
        self.description = ""   # Task description

        # Calculated values only for display purposes
        self.porc, self.porc_id = 0, 0
        self.count_total_tasks, self.count_completed_tasks = 0, 0

        self.soft_delete = False  # Flag for soft deletion of the task

        # Popups associated with this screen
        self.popup_time = PopupSelectTime()
        self.popup_work = PopupEditWork()
        self.dialog = None

    def on_enter(self, *args):
        self.update_label_texts_on_enter()
        self.soft_delete = self.tarea.soft_delete

    def on_leave(self, *args):
        self.ids.icon_text_hora.text = "Hour: "
        self.ids.icon_text_tarea.text = ""

    #   ===============================================================================
    #                           BUTTONS FUNCTIONS
    #   ===============================================================================
    def arrow_back_callback(self):
        """
        Notes:
            This is called when the arrow left icon in the top bar is pressed.
            It navigates back to the main screen.
        """
        MDApp.get_running_app().root.current = "main"

    def edit_handle(self):
        """
        This method is called when the edit button is pressed and performs different actions depending on the "edit_mode".

        Notes:
            - If in edit mode and there are changes to apply, it updates the task with the new data.
            - Otherwise, it toggles the edit mode and changes the background color to indicate the mode.
        """
        if self.edit_mode and self.apply_changes:
            # Set apply_changes to False as we are exiting this mode
            self.apply_changes = False

            # Create a new task object with updated data
            task_update = Tarea.create(list_days=self.list_days, desc=self.description,
                                       hour=self.hour, minute=self.minute,
                                       edit_mode=True, tarea_obj=self.tarea)

            # Update the task in the app's task list
            app_main = MDApp.get_running_app()
            app_main.list_tasks[self.tarea.id] = task_update

            # Get the main screen and history screen for do it changes
            main_screen = app_main.root.get_screen("main")
            history_screen = main_screen.ids.history_screen

            # Update the widget in the todo_list of main_screen
            main_screen.ids.todo_list.update_widget_in_todo_list(task_update)

            # Update the widget in the selection_list in history_screen
            history_screen.ids.selection_list.update_widget_in_todo_list(task_update)

            # Update the widget in the selection_list in history_screen
            all_tasks_screen = MDApp.get_running_app().root.get_screen("all_tasks_screen")
            all_tasks_screen.ids.selection_all_list.update_widget_in_todo_list(task_update)

            # change to this screen
            app_main.root.current = "main"

            # Save the new results
            save_wb_task_data()

        # Toggle edit mode and change background color to indicate the mode
        self.edit_mode = not self.edit_mode

    def delete_handle(self):
        """
        This method is called when the "Delete Button" is pressed.

        If the task's soft delete is True, my action will be to change its state to False and recover the task.

        If the task's soft delete is False and edit mode is True, I will set soft delete to True and make
        calls to methods to remove the task card from the todo_list in main_screen and from the todo_list
        in history_screen.

        :return: None
        """

        if self.soft_delete:
            # This actions continues in self.create_dialog

            # This is for stop button action
            return

        if self.edit_mode:
            app_main = MDApp.get_running_app()

            # Change the state to perform soft delete
            app_main.list_tasks[self.tarea.id].soft_delete = True

            # Call main_screen to remove the widget
            main_screen = app_main.root.get_screen("main")
            history_screen = main_screen.ids.history_screen

            # For remove de widget in todo_list in main screen
            main_screen.ids.todo_list.remove_widget_from_todo_list(self.tarea)

            history_screen.ids.selection_list.remove_widget_from_todo_list(self.tarea)
            history_screen.listar_callback()

            # Switch to main screen
            app_main.root.current = "main"

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
                                  If not provided, default values ("Yes", "No") are used.

        Notes:
            - If `list_buttons` is not provided, default button labels ("Yes", "No") are used.
            - The dialog is created and opened only if it does not already exist.
            - Button actions are bound to methods for handling dialog actions and closure.
            - `on_pre_dismiss` is bound to `self.dialog_reset` to reset dialog state before closing.
            - The first button is bound to `self.dialog_delete_handle` to handle the delete action.
            - The second button is bound to `self.dialog_close` to close the dialog without any action.
        """
        if list_buttons is None:
            list_buttons = ("Yes", "No")

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
                        on_release=self.dialog_delete_handle,
                    ),
                    MDFlatButton(
                        text=list_buttons[1],
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.dialog_close,
                    ),
                ],
            )
            self.dialog.open()

    def dialog_delete_handle(self, *args, **kwargs):
        app_main = MDApp.get_running_app()

        # Change the state to recover the task by modifying the soft delete
        app_main.list_tasks[self.tarea.id].soft_delete = False
        self.soft_delete = False

        # Add TareaCard in selection list to view.
        # Add the task widget to the dictionary of widgets with its ID as the key
        task = app_main.list_tasks[self.tarea.id]
        tarea_card = TareaCard(task, is_open=True)
        tarea_card2 = TareaCard(task, is_open=True)

        # Update todo_list main_screen
        main_screen = app_main.root.get_screen("main")
        main_screen.ids.todo_list.add_widget_in_todo_list(tarea_card)

        # Update selection_list history_screen
        history_screen = main_screen.ids.history_screen
        history_screen.ids.selection_list.add_widget_in_todo_list(tarea_card2)
        # history_screen.listar_callback()

        # To close dialog and reset
        self.dialog_close()

        # Switch to main screen
        app_main.root.current = "main"

        # Save the new results
        save_wb_task_data()

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

    # ===============================================================================
    #                           INTO TO INFO TASK SCREEN
    # ===============================================================================
    def update_info_task_screen(self, tarea):
        """
        Updates the Info Task screen with the provided task data.

        :param tarea: The Task object passed when the task label button is pressed.

        Notes:
            - Updates all necessary data and attributes within the screen for more organized functionality.
            - This function is called from the main_screen, which contains the todo_list.
        """

        # Assign tarea to the current task, and set list_days from the task's list_days attribute.
        self.tarea = tarea
        self.list_days = tarea.list_days

        # Calculate the percentage of completed tasks, total tasks, and a percentage ID
        # associated with an integer used later in the .kv file to access a specific image.
        self.porc, self.count_total_tasks, self.porc_id = calcular_porcentaje_tupla(self.tarea.list_repeat)
        self.count_completed_tasks = len(self.tarea.list_repeat)

        # Clear the grid buttons to avoid creating multiple instances of the object at the same time.
        self.ids.grid_buttons.clear_widgets()
        self.ids.cont_grid_buttons.add_widget(GridButtonsDay(self.list_days))

    #   ===============================================================================
    #                           UPDATE LABEL TEXTS
    #   ===============================================================================
    def update_label_hour(self, hours_value, minutes_value):
        """
        Updates the hour and minute labels on the screen based on the provided values.

        :param hours_value: (int) The hour value to be set.
        :param minutes_value: (int) The minute value to be set.
        :return: None

        Notes:
            - This function is called when "Accept" is pressed in the popup select_time.
            - It updates the hour and minute information displayed on the screen by changing the
              screen's attributes and setting the apply_changes flag to True, indicating that changes
              have been applied.
        """
        self.hour = int(hours_value)
        self.minute = int(minutes_value)
        combined_value = f"{hours_value:02d}:{minutes_value:02d}"
        self.ids.icon_text_hora.text = f"Hour: {combined_value}"
        self.apply_changes = True

    def update_label_tarea_text(self, text):
        """
        Updates the task description and title displayed on the screen with the provided text.

        :param text: (str) The new task description that has been edited.
        :return: None

        Notes:
            - Updates the `description` attribute with the new `text`.
            - Sets the `apply_changes` flag to True to indicate that changes have been made.
            - Updates the UI elements to reflect the new task description.
        """
        self.ids.icon_text_tarea.text = f"{text}"
        self.ids.top_bar_iw.title = text
        self.apply_changes = True
        self.description = text

    def update_label_texts_on_enter(self):
        """
        Updates all text elements within the screen when entering it.

        :return: None

        Notes:
            - This method updates all the text elements on the screen.
            - It assumes that a task is always present when entering this screen, so it does not check
            if `self.tarea` is None.
            - The condition to check if `self.tarea` is None is included to prevent potential errors,
            though it should not be necessary.
        """
        self.ids.top_bar_iw.title = f"{self.tarea.description}"

        combined_value = f"{self.tarea.hour:02d}:{self.tarea.minute:02d}"
        self.ids.icon_text_hora.text += f"{combined_value}"

        self.ids.icon_text_tarea.text = f"{self.tarea.description}"

        # This is the default display text but can be customized from the .kv file
        if self.count_completed_tasks > 10:
            self.ids.label_text_image.text = f"{self.porc}%"
            self.ids.label_text_cumplidas.text = (f"Tasks completed: "
                                                  f"{self.count_total_tasks}/{self.count_completed_tasks}")
        else:
            self.ids.label_text_image.text = f"JUST DO IT"
            self.ids.label_text_cumplidas.text = f"Continue with this Task for results!"


def calcular_porcentaje_tupla(list_repeat) -> tuple[int, int, int]:
    """
    Calculates the percentage of completed tasks, the total number of completed tasks,
    and a progress classification.

    :param list_repeat: List representing the number of times each task has been completed.
        A value of `1` in the list indicates that a task has been completed.

    :return: A tuple with three values:
        - `porc` (int): Percentage of completed tasks relative to the total number of tasks.
        - `total_cumplidas` (int): Total number of completed tasks.
        - `porc_id` (int): Progress identifier based on the percentage of completed tasks:
            - `0` for `0%` completed or if fewer than 10 tasks have been completed.
            - `1` for `1%` to `20%` completed.
            - `2` for `21%` to `40%` completed.
            - `3` for `41%` to `60%` completed.
            - `4` for `61%` to `80%` completed.
            - `5` for `81%` to `100%` completed.

    Notes:
        - If the length of `list_repeat` is less than or equal to 10, `porc_id` is returned as `0`.
        - The percentage (`porc`) is calculated as `(total_cumplidas * 100) // total_tareas`.
    """

    total_tareas = len(list_repeat)
    total_cumplidas = len([1 for tarea in list_repeat if tarea == 1])

    porc = total_cumplidas * 100 // total_tareas

    porc_id = \
        0 if porc == 0 or total_cumplidas <= 10 else \
        1 if porc <= 20 else \
        2 if porc <= 40 else \
        3 if porc <= 60 else \
        4 if porc <= 80 else \
        5  # 80% and above

    return porc, total_cumplidas, porc_id


def binary_search(list_today, task_id) -> int:
    """
    # esta fue la segunda idea despues de la busqeuda binaria pero al final encontre otra mejor ..
        Notes: Si bien el enfoque del diccionario me parecía rapido y accesible me di cuenta
        que puedo usar directamente los propios id, y hacer un poco de logica de herencia para relacionar
        los distintos conceptos sin necesidad de un diccionario

        # Hago una verificación previa si efectivamente existe el ID como key en el diccionario
        # aunque realmente yo sé que va a existir podría sacar esta condición
        if self.tarea.id in app_main.dict_tasks_today:
            # Modifico directamente en el diccionario dict_tasks_today en el key que correspondo al ID.
            # este enfoque tiene una complejidad de O(1)
            app_main.dict_tasks_today[self.tarea.id] = self.tarea
    """

    """
    # este era el anterior enfoque.
        # Preparo las variables para realizar la búsqueda binaria y la eventual modificación en la lista
        # de hoy para realizar los cambios en main_screen
        lista_to_edit = app_main.list_tasks_today
        id_to_search = app_main.list_tasks[self.tarea.id].id
        pos = binary_search(lista_to_edit, id_to_search)
        app_main.list_tasks_today[pos] = self.tarea

    Notes:
        Debido a que yo se que previamente esta lista esta ordenada por ID debería usar una busqueda binaria
        para que su complejidad sea de O(log(n))

        Si bien este enfoque lo voy a dejar de usar porque ahora uso un diccionario que tiene una complejidad
        de O(1) lo voy a dejar a la funcion por las dudas si eventualmente tengo que usarla.

    :param list_today: Se refiere a una lista de hoy de la app
    :param id_search: es el ID que vamos a buscar
    :return: pos(Int) que se refiere a la posicion indice dentro de esta list_today.
    """
    izq, der = 0, len(list_today) - 1

    while der >= izq:
        c = (izq + der) // 2
        if list_today[c].id == task_id:
            return c
        elif list_today[c].id > task_id:
            der = c - 1
        else:
            izq = c + 1

    return -1
