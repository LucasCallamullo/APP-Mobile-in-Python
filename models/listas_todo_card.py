
from kivymd.uix.list import MDList
from models.tarea import save_wb_task_data


class BaseList(MDList):
    def __init__(self, **kwargs):
        super(BaseList, self).__init__(**kwargs)
        self.widgets_dict = {}  # Diccionario para indexar widgets

    def add_widget_in_todo_list(self, task_to_add):
        """
        :param task_to_add: The widget representing the task to be added(TareaCard).
        """
        # Remove the widget from its current parent if it has one
        if task_to_add.parent:
            task_to_add.parent.remove_widget(task_to_add)

        self.add_widget(task_to_add)

        # Adds a task to the dictionary using the task ID as the key.
        self.widgets_dict[task_to_add.tarea.id] = task_to_add

    def update_widget_in_todo_list(self, task_update):
        """
        Updates a widget in the todo_list based on the provided task update.

        :param task_update: The updated task object with new data.
        :return: None
        """
        # Get the widget from the dictionary using the task ID
        widget = self.widgets_dict.get(task_update.id)

        if widget:
            # Update the task reference in the widget
            widget.tarea = task_update

            # Call the method from TareaCard to update the widget's labels
            widget.update_texts_on_label()

            # Optionally reassign the updated widget to the dictionary
            # Dictionaries reference the object, so changes are reflected directly
            self.widgets_dict[task_update.id] = widget

            # Save the updated state to the binary file
            save_wb_task_data()

            print("Updated widget task:")
            print(widget.tarea)

    def remove_widget_from_todo_list(self, task_delete):
        """
        Removes the widget from the todo_list corresponding to the task ID.

        :param task_delete: The task object to be soft_deleted.
        :return: None
        """
        # Get the widget from the dictionary using the task ID
        widget = self.widgets_dict.get(task_delete.id)

        if widget:
            # Update the task reference in the widget for the soft delete state
            widget.tarea = task_delete

            # Save the updated state to the binary file
            save_wb_task_data()

            # Remove the widget from the todo_list
            self.remove_widget(widget)

            # Remove the widget from the dictionary
            del self.widgets_dict[task_delete.id]
