from kivymd.uix.screen import MDScreen

from models.day_button import *
from models.popup_time_select import *
from models.popup_edit_task import *
from models.tarea import *


class InfoWorkScreen(MDScreen):
    """
        Pantalla de trabajo.
    """
    # Son dos flags para determinar si estamos en el modo edición para editar la tarea
    # y por otro lado, para saber si realizamos cambios o no
    edit_mode = BooleanProperty(False)
    apply_changes = BooleanProperty(False)

    def __init__(self, **kwargs):
        """
            Constructor de la clase WorkScreen.

            Parameters:
            ----------
            kwargs : dict
                Argumentos clave para inicialización.
        """
        super(InfoWorkScreen, self).__init__(**kwargs)

        self.tarea = None

        self.list_days = [False] * 7
        self.hour = -1
        self.minute = -1
        self.description = ""

        # Se calculan solo para mostrarse en pantalla
        self.porc, self.porc_id = 0, 0
        self.count_total_tasks, self.count_completed_tasks = 0, 0

        # PopUp asociados a esta pantalla
        self.popup_time = PopupSelectTime()
        self.popup_work = PopupEditWork()

    def on_enter(self, *args):
        self.update_label_texts_on_enter()

    def on_leave(self, *args):
        self.ids.icon_text_hora.text = ""
        self.ids.icon_text_tarea.text = ""

    #   ===============================================================================
    #                           BUTTONS FUNCTIONS
    #   ===============================================================================
    def arrow_back_callback(self):
        """
            Notes:
                Esta se llama al tocar el icono arrow left en la top bar es para volver a main
        """
        MDApp.get_running_app().root.current = "main"

    def delete_handle(self):
        if self.edit_mode:
            # Realizo el cambio dentro de la lista de la app que contiene la totalidad del archivo binario
            #  casualmente los id coinciden con el índice de la lista, por eso lo que estoy haciendo es actualizar
            #  sus datos en ese elemento en particular, para eventualmente realizar el guardado
            app_main = MDApp.get_running_app()
            app_main.list_tasks[self.tarea.id].soft_delete = True

            main_screen = app_main.root.get_screen("main")
            main_screen.remove_widget_from_todo_list(self.tarea)
            app_main.root.current = "main"

    def edit_handle(self):
        """
            Notes:
                Se llama al tocar editar dependiendo el caso del "edit_mode" realizar una accion u otra
        """
        if self.edit_mode and self.apply_changes:
            print("entre aca xd")

            # Cambio su apply_changes a False ya que salgo de este modo
            self.apply_changes = False

            # crea un nuevo objeto tarea con los datos actualizados
            task_update = Tarea.create(list_days=self.list_days, desc=self.description,
                                       hour=self.hour, min=self.minute,
                                       edit_mode=True, tarea_obj=self.tarea)

            # Realizo el cambio dentro de la lista de la app que contiene la totalidad del archivo binario
            #  casualmente los id coinciden con el índice de la lista, por eso lo que estoy haciendo es actualizar
            #  sus datos en ese elemento en particular, para eventualmente realizar el guardado
            app_main = MDApp.get_running_app()
            app_main.list_tasks[self.tarea.id] = task_update

            main_screen = app_main.root.get_screen("main")

            # Por ahora es la solucion que encontre a actualizar la lista del historial
            # aunque tengo que buscar otras.
            if main_screen.ids.history_screen.edit_mode:
                main_screen.ids.history_screen.listar_callback()
                app_main.root.current = "main"
                main_screen.ids.bottom_nav.switch_tab("history_task_tab")

            main_screen.update_widget_in_todo_list(task_update)
            app_main.root.current = "main"

        # Cambia su modo al tocarse asi mismo, a True o False tambien se ve representado porque cambia de color
        # su background
        self.edit_mode = not self.edit_mode

    #   ===============================================================================
    #                           INTO TO INFO TASK SCREEN
    #   ===============================================================================
    def update_info_task_screen(self, tarea):
        """
        :param: tarea(objeto) se refiere a una Tarea que trae consigo misma al tocar el boton label que la contiene

        Notes:
            actualizo todos los datos necesarios dentro de la pantalla ademas de atributos es para relizar un
            funcionamiento mas ordenado
            la funcion se llama desde main_screen que contiene al todo_list
        """

        # Igualamos tarea y tarea_edit, donde tarea va a ser la inicial, y tarea_edit va a ser la modificada
        # en caso de efectuar los cambios sino conservamos los datos originales
        self.tarea = tarea
        self.list_days = tarea.list_days

        # Calculamos el porcentaje de las tareas cumplidas, la cantidad que se cumplieron, y un porc_id
        # asociado a un número entero que después usamos como índice en el .kv para acceder a un IMG en particular
        self.porc, self.count_total_tasks, self.porc_id = calcular_porcentaje_tupla(self.tarea.list_repeat)
        self.count_completed_tasks = len(self.tarea.list_repeat)

        # tengo que hacer esto para que no se creen dos instancias del objeto al mismo tiempo
        self.ids.grid_buttons.clear_widgets()
        self.ids.cont_grid_buttons.add_widget(GridButtonsDay(self.list_days))

    #   ===============================================================================
    #                           UPDATE LABEL TEXTS
    #   ===============================================================================
    def update_label_hour(self, hours_value, minutes_value):
        """
        :param hours_value: (int)
        :param minutes_value: (int)
        :return:
        Notes:
            Es solamente una funcion que se llama cuando se toca "Aceptar" en el popup select_time sirve
            para actualizar la info en pantalla de la hora y minutos, se cambia los atributos propios
            de la pantalla y tambien se cambia la bandera de applychanges diciendo que efectivamente
            aplicamos cambios
        """
        self.hour = int(hours_value)
        self.minute = int(minutes_value)
        combined_value = f"{hours_value:02d}:{minutes_value:02d}"
        self.ids.icon_text_hora.text = f"{combined_value}"
        self.apply_changes = True

    def update_label_tarea_text(self, text):
        """
        :param text: (str) se refiere a la nueva tarea actualizada que editamos
        :return:
        Notes:
            cambiamos el atributo description por este nuevo text, ademas cambiamos la bandera que indica
            que efectivamente realizamos cambios
        """
        self.ids.icon_text_tarea.text = f"{text}"
        self.ids.top_bar_iw.title = text
        self.apply_changes = True
        self.description = text

    def update_label_texts_on_enter(self):
        """
            :return:
            Notes:
                Esto es solo para actualizar todos los text dentro de la screen, en este caso no voy a hacer la
                verifiacion de si tiene o no una tarea porque deberia de tenerla siempre cuando entra aca
                por lo tanto dejo la condicion para evitar errores pero no debería pasar nunca
                if self.tarea is None: return
        """
        self.ids.top_bar_iw.title = f"{self.tarea.description}"

        combined_value = f"{self.tarea.hour:02d}:{self.tarea.minute:02d}"
        self.ids.icon_text_hora.text += f"{combined_value}"

        self.ids.icon_text_tarea.text = f"{self.tarea.description}"

        # Esto es lo que se muestra por defecto, pero es personalizable desde el .kv
        if self.count_completed_tasks > 10:
            self.ids.label_text_image.text = f"{self.porc}%"
            self.ids.label_text_cumplidas.text = (f"Tasks completed: "
                                                  f"{self.count_total_tasks}/{self.count_completed_tasks}")
        else:
            self.ids.label_text_image.text = f"JUST DO IT"
            self.ids.label_text_cumplidas.text = f"Continue with this Task for results!"


def calcular_porcentaje_tupla(list_repeat) -> tuple[int, int, int]:
    """
    Calcula el porcentaje de tareas cumplidas, la cantidad total de tareas cumplidas
    y una clasificación del progreso.

    :param: list_repeat: Lista que representa la cantidad de veces que se ha realizado cada tarea.
        Se asume que el valor `1` en la lista indica que una tarea ha sido cumplida.

    :return: Una tupla con tres valores:
        - `porc` (int): Porcentaje de tareas cumplidas con respecto al total de tareas.
        - `total_cumplidas` (int): Cantidad total de tareas cumplidas.
        - `porc_id` (int): Identificador de progreso basado en el porcentaje de tareas cumplidas:
            - `0` para `0%` cumplido o si hiciste menos de 10 tareas cumplidas.
            - `1` para `1%` a `20%` cumplido.
            - `2` para `21%` a `40%` cumplido.
            - `3` para `41%` a `60%` cumplido.
            - `4` para `61%` a `80%` cumplido.
            - `5` para `81%` a `100%` cumplido.

    Notes:
        - Si la longitud de `total_cumplidas` es menor o igual a 10, se devuelve `0` por porc_id.
        - El porcentaje (`porc`) se calcula como `(total_cumplidas * 100) // total_tareas`.
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
        5  # 80% >

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
