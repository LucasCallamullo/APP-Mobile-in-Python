

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager

# Aca van mis modulos importados
from screens.main_screen import MainScreen
from screens.task_screen import AddTaskScreen
from screens.task_info_screen import InfoWorkScreen
from screens.task_history_screen import TaskHistoryScreen
from screens.task_alls_screen import AllTasks

from models.tarea_card import TareaCard
from models.tarea import load_rb_task_data

# This is for setting the window size similar to a cellphone
# from kivy.core.window import Window
# Window.size = (350, 600)


def load_kv_files():
    """ Loads the necessary .kv files for the application. """
    Builder.load_file('kv/main_screen.kv')
    Builder.load_file('kv/task_screen.kv')
    Builder.load_file('kv/task_info_screen.kv')
    Builder.load_file('kv/task_history_screen.kv')
    Builder.load_file('kv/task_alls_screens.kv')


class ToDoApp(MDApp):

    def build(self):
        """
        Notes:
            Builds the application's interface by loading the KV files and configures the ScreenManager.

        Attributes:
            self.list_tasks: A list created that contains all tasks from the file. This is used both
            to save to the binary file and to make modifications during the various events of the program:
            creating, editing, saving, deleting tasks.
        """
        load_kv_files()

        self.list_tasks = load_rb_task_data()

        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.material_style = "M3"
        # self.theme_cls.primary_palette = "Cyan"
        # self.dict_today = {}

        screen_manager = MDScreenManager()
        screen_manager.add_widget(MainScreen(name='main'))
        screen_manager.add_widget(AddTaskScreen(name='add_task'))
        screen_manager.add_widget(InfoWorkScreen(name='info_task'))
        screen_manager.add_widget(TaskHistoryScreen(name='history_task'))
        screen_manager.add_widget(AllTasks(name='all_tasks_screen'))
        return screen_manager

    def on_start(self):
        """
        Reason for Creating Multiple Instances of TareaCard
        Unique Parent Restriction:
            In Kivy, each widget can only have one parent. If you try to add the same widget to
            two different parents, an error will occur because Kivy does not allow a widget to
            have multiple parents. Therefore, you need to create separate instances of TareaCard
            for each container.

        Independent Visualization:
            Each instance of TareaCard you create for a container (e.g., todo_list, selection_list,
            selection_all_list) is an independent copy of the widget. This ensures that each container
            has its own representation of the TareaCard, and each can be managed and updated independently.

        Avoiding Duplicate Widget Error:
            If you try to reuse the same widget in different places, you will get an error like
            the one you mentioned: WidgetException: Cannot add <widget> it already has a parent.
            Creating new instances avoids this problem.

        Optimization by Reducing Loop Iterations:
            I reached this conclusion to avoid having to loop through the task list three times.
            By creating multiple instances of TareaCard in a single loop, I can optimize the process
            and achieve the desired functionality more efficiently.

        :return:
            Filters the active tasks for today that are not deleted to show them on the "main_screen".
            Also, creates the TareaCard for each task to serve as a container for the various task actions.

        Notes:
            - The logic is that if the day corresponding to Today is True, it means it should be displayed.
              If it is False, it simply won't be shown on the "main" screen.
            - Deleted tasks are also omitted, respecting the soft delete functionality.
        """

        if not self.list_tasks:
            return

        main_screen = MDApp.get_running_app().root.get_screen("main")

        # create selection_list with this
        history_screen = main_screen.ids.history_screen
        # history_screen.listar_callback()

        # Create selection_all_list with this
        all_tasks_screen = MDApp.get_running_app().root.get_screen("all_tasks_screen")
        # all_tasks_screen.listar_all_callback()

        for task in self.list_tasks:

            # This is for view of all tasks independent of is soft_delete or not
            task_to_add3 = TareaCard(task, True)
            all_tasks_screen.ids.selection_all_list.add_widget_in_todo_list(task_to_add3)

            # Skip the task if soft_delete is True, meaning it is deleted.
            # This is an approach towards "soft delete".
            if task.soft_delete:
                continue

            # This is for view of all tasks if is not soft_delete
            task_to_add2 = TareaCard(task, True)
            history_screen.ids.selection_list.add_widget_in_todo_list(task_to_add2)

            # This means only tasks for today are shown.
            if task.list_days[main_screen.today_id]:
                # Retrieve the task and add it to the todo_list presentation in main_screen.
                task_to_add = TareaCard(task, True)
                main_screen.ids.todo_list.add_widget_in_todo_list(task_to_add)


if __name__ == '__main__':
    ToDoApp().run()
