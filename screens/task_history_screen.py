
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


from kivy.animation import Animation
from kivy.utils import get_color_from_hex

from models.tarea_card import *


from kivymd.uix.selection import MDSelectionList


class ListHistory(MDSelectionList):
    def __init__(self, task=None, **kwargs):
        super(ListHistory, self).__init__(**kwargs)
        self.widgets_dict = {}  # Diccionario para indexar widgets


class TaskHistoryScreen(MDScreen):
    """
        Pantalla de trabajo.
    """
    overlay_color = get_color_from_hex("#6042e4")

    def __init__(self, **kwargs):
        """
            Constructor de la clase WorkScreen.

            Parameters:
            ----------
            kwargs : dict
                Argumentos clave para inicialización.
        """
        super(TaskHistoryScreen, self).__init__(**kwargs)
        self.edit_mode = False
        self.list_task_to_delete = []

    def edit_mode_off(self):
        self.edit_mode = False

    def listar_callback(self):

        list_works = MDApp.get_running_app().list_tasks

        self.ids.selection_list.clear_widgets()
        self.edit_mode = True

        for i in list_works:

            if i.soft_delete:
                continue

            task = TareaCard(i, True)
            self.ids.selection_list.add_widget(task)
            self.ids.selection_list.widgets_dict[task.id] = task

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
            left_action_items = [["menu"]]
            right_action_items = [["magnify"], ["dots-vertical"]]
            self.ids.toolbar.title = "Inbox"

        Animation(md_bg_color=md_bg_color, d=0.2).start(self.ids.toolbar)
        self.ids.toolbar.left_action_items = left_action_items
        self.ids.toolbar.right_action_items = right_action_items

    def on_selected(self, instance_selection_list, instance_selection_item):
        """
        Callback para el evento de selección de un ítem en la lista.

        Parameters:
        ----------
        instance_selection_list : MDSelectionList
            La instancia de la lista de selección en la que se realizó la selección.
        instance_selection_item : SelectionItem
            La instancia del ítem seleccionado en la lista de selección.

        Actions:
        --------
        - Actualiza el título de la barra de herramientas con el número de ítems seleccionados.
        - Agrega el ítem seleccionado a `list_task_to_delete`.
        """
        self.ids.toolbar.title = str(
            len(instance_selection_list.get_selected_list_items())
        )

        # esto es para obtener la lista si quisiera lo dejo comentado por las dudas algun día lo uso
        # selected_items = instance_selection_list.get_selected_list_items()

        # aca obtengo el item seleccionado y lo agrego a list_Task_to_delete
        tarea_card = instance_selection_item.instance_item
        self.list_task_to_delete.append(tarea_card)

    def on_unselected(self, instance_selection_list, instance_selection_item):
        """
        Callback para el evento de deselección de un ítem en la lista.

        Parameters:
        ----------
        instance_selection_list: MDSelectionList
            La instancia de la lista de selección en la que se realizó la deselección.
        instance_selection_item: SelectionItem
            La instancia del ítem deseleccionado en la lista de selección.

        Actions:
        --------
        - Actualiza el título de la barra de herramientas con el número de ítems seleccionados.
        - Elimina la tarea correspondiente de `list_task_to_delete` si el ítem es desmarcado.
        """
        if instance_selection_list.get_selected_list_items():
            self.ids.toolbar.title = str(
                len(instance_selection_list.get_selected_list_items())
            )

        # Esta es la forma de acceder al item seleccionado y sus atributos los que tuviera
        # en este caso nos referimos a TareaCard
        tarea_card_unselected = instance_selection_item.instance_item

        # Elimina el ítem deseleccionado de la lista de tareas a eliminar usando comprensión de listas.
        self.list_task_to_delete = [i for i in self.list_task_to_delete if i.tarea.id != tarea_card_unselected.tarea.id]

        """
        Alternativamente, se puede utilizar el método `remove` de la lista para eliminar el ítem deseleccionado:
        
        for i in self.list_task_to_delete:
            if i.id == item_unselected.tarea.id:
                self.list_task_to_delete.remove(i)
                break
        """

    def delete_list_handle(self):
        """
        Maneja la eliminación de las tareas seleccionadas en la lista de tareas.

        Obtiene la lista general de tareas de la aplicación, marca las tareas seleccionadas
        como eliminadas mediante el atributo `soft_delete`, y guarda los datos de todas las
        tareas modificadas. Luego, llama a la función para actualizar la lista de tareas en la
        página de historial y reinicia la lista de tareas a eliminar para la próxima vez que
        se llame a la función `on_selected`.

        Pasos:
        1. Obtiene la instancia de la aplicación en ejecución.
        2. Itera sobre la lista de tareas seleccionadas.
        3. Marca cada tarea como eliminada.
        4. Guarda los datos de todas las tareas modificadas.
        5. Llama a la función para actualizar la lista de tareas en la página de historial.
        6. Reinicia la lista de tareas a eliminar.

        Returns:
            None
        """

        # Obtiene la instancia de la aplicación en ejecución
        app_main = MDApp.get_running_app()

        # Marca cada tarea como eliminada en la lista de tareas de la aplicación
        for tarea_card in self.list_task_to_delete:
            app_main.list_tasks[tarea_card.tarea.id].soft_delete = True

        # Guarda los datos de todas las tareas modificadas
        save_all_items(app_main.list_tasks)

        # Llama a la función para actualizar la lista de tareas en la página de historial
        self.listar_callback()

        # Reinicia la lista de tareas a eliminar para la próxima vez que se llame a `on_selected`
        self.list_task_to_delete = []

    def future_menu(self):
        pass


def save_all_items(list_to_save, fd='tareas.dat'):
    with open(fd, 'wb') as file:
        for task in list_to_save:
            pickle.dump(task.tarea, file)
            file.flush()