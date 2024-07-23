

import pickle

from kivymd.app import MDApp
from kivy.properties import BooleanProperty
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class TareaCard(TwoLineAvatarIconListItem):
    def __init__(self, tarea, is_open=False, **kwargs):
        """
        Parameters:
            ** kwargs: Argumentos clave para inicialización.
            tarea: es un objeto Tarea creado completo. (es decir ya paso por el create_task(cls)
            is_open: es para saber si estoy durante el programa(False) o iniciando(True)
            tarea_state: realmente tuve que crearlo para tener una instancia que pueda usar de variable para
                algunas condiciones en el diseño dentro del .kv

        Notes:
        """
        super(TareaCard, self).__init__(**kwargs)
        self.tarea = tarea
        self.tarea_state = self.tarea.state
        self.update_texts_on_label()

        self.dialog = None

        if not is_open:
            self.save_append_data()

    def __str__(self):
        return "hola tarea card"

    # =================================================================
    #               SAVE AND LOAD DATA FROM LISTS
    # =================================================================
    def save_append_data(self, fd='tareas.dat'):
        """
        Notes:
            Se llama cada vez que agreguemos una nueva tarea completa en este caso usamos el "ab"
            por una cuestión de que no hacer falta reescribir tod0 el archivo completo solamente agregar
            el nuevo elemento al final del archivo, tambien es para respetar el orden de los ID.
        :return:
        """
        # se hace este append, para que también se agregue a lista que corresponde al total de tareas.
        MDApp.get_running_app().list_tasks.append(self.tarea)

        with open(fd, 'ab') as file:
            pickle.dump(self.tarea, file)
            file.flush()
            print(self.tarea)

    def save_write_data(self, fd='tareas.dat'):
        """
        Notes:
            - Por ahora se llama cuando confirmamos con el CheckBox que realizamos la Task
            - Todavía puedo realizar alguna forma de verificar el estado solo una vez y que no se pueda modificar.

        """
        list_tasks = MDApp.get_running_app().list_tasks
        # en este caso reescribimos el archivo binario por completo con los datos actualizados.
        with open(fd, 'wb') as file:
            for task in list_tasks:
                pickle.dump(task, file)
                file.flush()

    # =================================================================
    #       Buttons Actions of Tarea Card
    # =================================================================
    def on_press(self, *args):
        """
        Notes:
            - Se llama asi misma cuando se toca el Label que contiene la Tarea en sí
            - Luego te redirige a la pantalla "info_task" para más info de la tarea, a su vez
            lleva una función propia update_info_task_screen de "info_task" para poder crear la
            pantalla con los datos necesarios.
        """
        main_screen = MDApp.get_running_app().root.get_screen("main")
        history_screen = main_screen.ids.history_screen

        if history_screen.edit_mode:
            return

        info_screen = MDApp.get_running_app().root.get_screen("info_task")
        info_screen.update_info_task_screen(self.tarea)
        MDApp.get_running_app().root.current = "info_task"

    def check_complete(self, i, value):
        """
        Args:
            i (int): El índice del checkbox. (poner si o si)
            value (bool): El estado del checkbox (True si está marcado, False si no).

        Notes:
            Actualiza el valor del tarea_state y del self.tarea.state que no son lo mismo recordemos.
            Uno es el estado del objeto tarea, y otro es del TareaCard
            - Pensar si guardar con save_data.
        """
        self.tarea.state = True if value else False
        self.tarea_state = self.tarea.state

        print("el self tarea.state es:", self.tarea.state)

    # =================================================================
    #       Updates Labels Texts.
    # =================================================================
    def update_texts_on_label(self):
        """
        Notes:
            Lo único que hace es actualizar los valores de texto y hora que se muestran.
        """
        self.text = self.tarea.description

        combined_value = f"{self.tarea.hour:02d}:{self.tarea.minute:02d}"
        self.secondary_text = combined_value

    # =================================================================
    #       REFERIDO A MD DIALOG
    # =================================================================
    def create_dialog(self, text_title="", text_label="", list_buttons=None):
        """
        Crea y muestra un diálogo genérico con botones personalizados.

        Args:
            text_title (str): Título del diálogo.
            text_label (str): Texto principal del diálogo.
            list_buttons (tuple): Lista de etiquetas para los botones.
                                  Si no se proporciona, se usan valores por defecto ("Completed", "Incomplete", "Cancel").

        """
        if list_buttons is None:
            list_buttons = ("Completed", "Incomplete", "Cancel")

        if not self.dialog:
            self.dialog = MDDialog(
                text=text_label,
                title=text_title,
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

        else:
            self.dialog = None

    def dialog_close(self, *args, **kwargs):
        """
        Cierra el diálogo actual y lo elimina.
        """
        self.dialog.dismiss()
        self.dialog = None

    def count_tasks_one(self, *args, **kwargs):
        """
        Marca la tarea como completada, la guarda en la lista de tareas y cierra el diálogo.
        """
        self.tarea.list_repeat.append(1)

        # Actualiza la lista de tareas en la aplicación principal.
        MDApp.get_running_app().list_tasks[self.tarea.id] = self.tarea

        self.dialog_close()

        # print("Probamos si guarda")
        print(self.tarea)

        # Guarda los cambios en los datos.
        self.save_write_data()

    def count_tasks_zero(self, *args, **kwargs):
        """
        Marca la tarea como incompleta, la guarda en la lista de tareas y cierra el diálogo.
        """
        self.tarea.list_repeat.append(0)

        # Actualiza la lista de tareas en la aplicación principal.
        MDApp.get_running_app().list_tasks[self.tarea.id] = self.tarea

        self.dialog_close()

        # Guarda los cambios en los datos.
        self.save_write_data()


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        """
        Inicializa el RightCheckbox.
        Notes:
            Se utiliza en la creación del Tarea Card es la forma de saber si realizamos una tarea o no
            - Obtiene su propio atributo active que es simplemente un bool
        """
        super(RightCheckbox, self).__init__(**kwargs)