

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from models.tarea_card import TareaCard
from models.listas_todo_card import BaseList


class ListHistoryAll(BaseList):
    def __init__(self, **kwargs):
        super(ListHistoryAll, self).__init__(**kwargs)
        # self.widgets_dict = {}  # Diccionario para indexar widgets
        # id: selection_all_list


class AllTasks(MDScreen):
    """
    Screen displaying all tasks including deletes and not deletes.
    """

    def __init__(self, **kwargs):
        super(AllTasks, self).__init__(**kwargs)

    def on_enter(self, *args):
        """
        Called when entering the AllTasks screen.

        This method:
        1. Calls `listar_all_callback` to populate the list with all tasks.
        2. Sets the `edit_mode` of the history screen to False.
        """

        main_screen = MDApp.get_running_app().root.get_screen("main")
        main_screen.ids.history_screen.edit_mode = False

        self.listar_all_callback()

    def on_leave(self, *args):
        main_screen = MDApp.get_running_app().root.get_screen("main")
        main_screen.ids.history_screen.edit_mode = True

    def listar_all_callback(self):
        """
        Populates the list with all tasks.

        This method:
        1. Retrieves the list of tasks from the application.
        2. Clears the widgets in the `selection_all_list`.
        3. Adds each task as a `TareaCard` to the `selection_all_list`.
        """

        # dictionary = self.ids.selection_all_list.widgets_dict
        # if dictionary:
        #    return

        list_works = MDApp.get_running_app().list_tasks

        self.ids.selection_all_list.clear_widgets()

        for i in list_works:

            # Create a new TareaCard widget for each task and add it to the selection list
            task = TareaCard(i, True)

            # Add TareaCard in selection list to view.
            # Add the task widget to the dictionary of widgets with its ID as the key
            self.ids.selection_all_list.add_widget_in_todo_list(task)

    def arrow_back_callback(self):
        """
        Called when the back arrow icon in the top bar is touched.

        This method:
        1. Switches the current screen to "main".
        """
        MDApp.get_running_app().root.current = "main"
