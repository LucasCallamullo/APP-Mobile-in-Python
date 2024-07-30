
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


from kivy.animation import Animation
from kivy.utils import get_color_from_hex

from models.tarea_card import TareaCard
from models.tarea import save_wb_task_data


from kivymd.uix.selection import MDSelectionList
from models.listas_todo_card import BaseList


class ListHistory(MDSelectionList, BaseList):
    def __init__(self, **kwargs):
        super(ListHistory, self).__init__(**kwargs)
        # self.widgets_dict = {}  # Diccionario para indexar widgets
        # id = selection_list, this is the ID on kv file


class TaskHistoryScreen(MDScreen):
    overlay_color = get_color_from_hex("#6042e4")

    def __init__(self, **kwargs):
        """
        Screen for displaying task history.
        Initializes the TaskHistoryScreen with default values.
        """
        super(TaskHistoryScreen, self).__init__(**kwargs)
        self.edit_mode = False
        self.list_task_to_delete = []

    def listar_callback(self):
        """
        Updates the list of tasks displayed on the screen.

        This method is called to populate the task history screen with task cards that are not
        marked for deletion.
        It clears any existing widgets from the selection list, sets the screen to edit mode,
        and then adds new task cards for each task in the list that is not marked as soft deleted.

        Notes:
            - Retrieves the list of tasks from the application.
            - Clears existing widgets from the selection list to prepare for new data.
            - Sets the screen to edit mode.
            - Iterates over the list of tasks and adds each task that is not marked as soft
            deleted to the screen.
        """
        # Clear existing widgets from the selection list to update with new tasks
        self.ids.selection_list.clear_widgets()

        dictionary = self.ids.selection_list.widgets_dict
        if dictionary:
            # key referencia a un indice? value is tarea card
            for key, tarea_card in dictionary.items():
                self.ids.selection_list.add_widget_in_todo_list(tarea_card)
            print("El diccionario contiene elementos.")
            return

        # Get the list of tasks from the running application
        list_works = MDApp.get_running_app().list_tasks
        for i in list_works:

            # Skip tasks that are marked for soft deletion
            if i.soft_delete:
                continue

            # Create a new TareaCard widget for each task and add it to the selection list
            task = TareaCard(i, True)

            # Add TareaCard in selection list to view.
            # Add the task widget to the dictionary of widgets with its ID as the key
            self.ids.selection_list.add_widget_in_todo_list(task)

    def delete_list_handle(self):
        """
        Handles the deletion of selected tasks from the task list.

        Retrieves the general list of tasks from the application, marks the selected tasks
        as deleted using the `soft_delete` attribute, and saves the data of all modified tasks.
        Then, it calls the function to update the task list on the history page and resets the
        list of tasks to delete for the next time the `on_selected` function is called.

        Steps:
        1. Retrieve the instance of the running application.
        2. Iterate over the list of selected tasks.
        3. Mark each task as deleted.
        4. Save the data of all modified tasks.
        5. Call the function to update the task list on the history page.
        6. Reset the list of tasks to delete.

        Returns:
            None
        """

        # Retrieve the instance of the running application
        app_main = MDApp.get_running_app()

        # Obtain the main screen to eventually update the todo_list of the main screen
        main_screen = app_main.root.get_screen("main")

        # Mark each task as deleted in the application's task list
        for tarea_card in self.list_task_to_delete:

            task = app_main.list_tasks[tarea_card.tarea.id]
            task.soft_delete = True
            # print(task)  # For debugging purposes

            # Remove the task from the todo_list on the main screen
            main_screen.ids.todo_list.remove_widget_from_todo_list(task)

            # Remove the widget from the dictionary for the next listar callback
            self.ids.selection_list.remove_widget_from_todo_list(task)

        # Call the function to update the task list on the history page
        self.listar_callback()

        # Reset the list of tasks to delete for the next time `on_selected` is called
        self.list_task_to_delete = []

        # Save the data of all modified tasks
        save_wb_task_data()

        # This is to exit the edit mode
        # self.ids.selection_list.unselected_all()

    def future_menu(self):
        print("aca va a ir un menu")

    def change_to_alltasks_screen(self):
        MDApp.get_running_app().root.current = "all_tasks_screen"

    def change_edit_mode(self):
        """ Disables edit mode for the screen. """
        self.edit_mode = not self.edit_mode
        print(self.edit_mode)

    # ===========================================================================
    #           ALL funcionts relative to Selected Mod
    # ===========================================================================
    def set_selection_mode(self, instance_selection_list, mode):
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [
                [
                    "close",
                    lambda x: self.ids.selection_list.unselected_all(),
                ]
            ]
            right_action_items = [["trash-can", lambda x: self.delete_list_handle()],
                                  ["dots-vertical"]]

        else:
            md_bg_color = (0, 0, 0, 1)
            left_action_items = [["menu", lambda x: self.future_menu()]]
            right_action_items = [["magnify", lambda x: self.change_to_alltasks_screen()],
                                  ["dots-vertical", lambda x: self.change_edit_mode()]]
            self.ids.toolbar.title = "Inbox"

        Animation(md_bg_color=md_bg_color, d=0.2).start(self.ids.toolbar)
        self.ids.toolbar.left_action_items = left_action_items
        self.ids.toolbar.right_action_items = right_action_items

    def on_selected(self, instance_selection_list, instance_selection_item):
        """
        Callback for the event when an item is selected from the list.

        Parameters:
            instance_selection_list : MDSelectionList
                The instance of the selection list where the selection was made.
            instance_selection_item : SelectionItem
                The instance of the selected item within the selection list.

        Actions:
            - Updates the toolbar title with the number of selected items.
            - Adds the selected item to the `list_task_to_delete`.
        """
        # Update the toolbar title with the count of selected items
        self.ids.toolbar.title = str(
            len(instance_selection_list.get_selected_list_items())
        )

        # This code retrieves the selected items list, left commented for future use if needed
        # selected_items = instance_selection_list.get_selected_list_items()

        # Get the selected item and add it to the `list_task_to_delete` list
        tarea_card = instance_selection_item.instance_item
        self.list_task_to_delete.append(tarea_card)

    def on_unselected(self, instance_selection_list, instance_selection_item):
        """
        Callback for the event when an item is deselected from the list.

        Parameters:
            instance_selection_list: MDSelectionList
                The instance of the selection list where the deselection was made.
            instance_selection_item: SelectionItem
                The instance of the deselected item within the selection list.

        Actions:
            - Updates the toolbar title with the number of selected items.
            - Removes the corresponding task from `list_task_to_delete` if the item is unchecked.
        """
        # Update the toolbar title with the count of remaining selected items
        if instance_selection_list.get_selected_list_items():
            self.ids.toolbar.title = str(
                len(instance_selection_list.get_selected_list_items())
            )

        # Access the deselected item and its attributes, referring to TareaCard
        tarea_card_unselected = instance_selection_item.instance_item

        # Remove the deselected item from the list of tasks to delete using list comprehension
        self.list_task_to_delete = [i for i in self.list_task_to_delete if i.tarea.id != tarea_card_unselected.tarea.id]

        """
        Alternatively, the `remove` method can be used to remove the deselected item:

        for i in self.list_task_to_delete:
            if i.tarea.id == tarea_card_unselected.tarea.id:
                self.list_task_to_delete.remove(i)
                break
        """