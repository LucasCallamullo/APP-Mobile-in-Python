

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager

# Aca van mis modulos importados
import pickle

from screens.main_screen import *
from screens.task_screen import *
from screens.task_info_screen import *
from screens.task_history_screen import *
from models.tarea import *
from models.tarea_card import *

# esto es para el tamaño de la ventana similar a un celular
from kivy.core.window import Window
Window.size = (350, 600)


class ToDoApp(MDApp):

    def build(self):
        """
        Notes:
            - Construye la interfaz de la aplicación cargando los kv y configura el ScreenManager.

        :Attributes:
            self.list_tasks: Es una lista creada que contiene al total del archivo, esto sirve tanto para
            guardar en el archivo binario, como recuperar el diccionario dict_task_today
        """
        load_kv_files()

        self.list_tasks = []
        self.load_data()
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.material_style = "M3"
        # self.theme_cls.primary_palette = "Cyan"

        screen_manager = MDScreenManager()
        screen_manager.add_widget(MainScreen(name='main'))
        screen_manager.add_widget(AddTaskScreen(name='add_task'))
        screen_manager.add_widget(InfoWorkScreen(name='info_task'))
        screen_manager.add_widget(TaskHistoryScreen(name='history_task'))
        return screen_manager

    def on_start(self):
        """
        :return:
            list_tasks_today = Hace referencia a lista de hoy que se filtraron para agregar al widget

        Notes:
            - La lógica es que si el día que corresponda a HOY esta en True significa que entonces debe mostrarse
            si estuviera en False simplemente no se mostrará en la Screen "main"
            - También omitimos los task eliminados, por el soft delete
        """
        if not self.list_tasks:
            return

        main_screen = MDApp.get_running_app().root.get_screen("main")
        for i in self.list_tasks:

            # Omitimos el registro si esta soft_delete = True, ya que significaría que esta eliminado,
            # este es un enfoque hacia el "soft delete".
            if i.soft_delete:
                continue

            # Solo se agregan a dict_task_today los que estén en True en el día especificado de hoy.
            # Es decir solo se muestran las tareas que son de hoy.
            if i.list_days[main_screen.today_id]:

                # recupero la tarea y lo agrego a la presentación en todo_list
                task_to_add = TareaCard(i, True)
                main_screen.add_widget_in_todo_list(task_to_add)

    def load_data(self, fd='tareas.dat'):
        """
            Carga los datos de tareas desde un archivo pickle.

        Parameters:
            fd: str, optional
                Nombre del archivo desde donde cargar los datos. Por defecto es 'tareas.dat'.

        Raises:
            FileNotFoundError
                Si el archivo especificado (`fd`) no existe en el sistema, devuelve dos listas vacías.

        :return:
            list_tasks = Hace referencia a lista del total de las Tasks

        Notes:
            Leer objetos binarios desde pickle y usando el "EOFError" como condicion de corte del puntero
            del archivo sin necesidad de un .tell().

        """
        # list_tasks = []
        try:
            with open(fd, 'rb') as file:
                while True:
                    try:

                        task_recovery = pickle.load(file)
                        self.list_tasks.append(task_recovery)
                        print(task_recovery)
                    except EOFError:
                        break

        except FileNotFoundError:
            print(f"El archivo {fd} no existe.")

        # return list_tasks


def load_kv_files():
    """ Carga los archivos .kv necesarios para la aplicación.   """
    Builder.load_file('kv/main_screen.kv')
    Builder.load_file('kv/task_screen.kv')
    Builder.load_file('kv/task_info_screen.kv')
    Builder.load_file('kv/task_history_screen.kv')


if __name__ == '__main__':
    ToDoApp().run()

