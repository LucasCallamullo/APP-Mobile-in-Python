

from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.color_definitions import colors

from kivy.properties import ListProperty, BooleanProperty

from models.snackbar_generic import *


class GridButtonsDay(MDGridLayout):
    """
        * creo que todavía se podría mejorar la creacion del diccionario para que sean 7 vueltas en vez de 14
        pero de momento lo voy a dejar asi
        * tambien debería ver como pasar como parametro desde el .kv una lista con los nombres de los iconos
        para poder utilizar en este constructor, aunque creo que debería pasarlo por el workscreen primero revisar
    """
    def __init__(self, lista_active=None, **kwargs):
        """
        Constructor de GridButtonsDay.

        Este constructor inicializa un diccionario para facilitar la creación genérica de botones
        para cada día de la semana. Los botones son añadidos al layout al momento de la creación del objeto.

        Notas:
            - Se usa un diccionario para almacenar el estado, ícono e ID de cada día.

        Parámetros:
            **kwargs: Argumentos clave para inicialización.
        """
        super(GridButtonsDay, self).__init__(**kwargs)
        self.cols = 7
        self.lista_active = [False] * 7 if lista_active is None else lista_active

        list_days_icon = ("alpha-l-circle", "alpha-m-circle", "alpha-m-circle",
                          "alpha-j-circle", "alpha-v-circle", "alpha-s-circle", "alpha-d-circle")

        list_days_id = ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday")

        self.days_dict = {
            day: {
                "active": active,
                "icon": icon,
                "id": day_id,
                "id_num": num
            }
            for day, active, icon, day_id, num in
            zip(list_days_id, self.lista_active, list_days_icon, list_days_id, range(7))
        }

        for day, info in self.days_dict.items():
            self.add_widget(
                DayButton(icon=info["icon"],
                          id=info["id"],
                          active=info["active"],
                          id_num=info["id_num"],
                          md_bg_color=colors["Blue"]["500"] if info["active"] else colors["BlueGray"]["600"]))

    def change_list_dicts(self, day_button):
        """
        Actualiza el diccionario de días con el estado actual del botón de día.

        :param day_button: El botón de día cuya información se va a actualizar.
        :type day_button: DayButton
        :return: None
        Notes:
            Se utiliza un diccionario para acceder directamente al estado del día con una velocidad de O(1),
            en lugar de iterar a través de una lista, lo que tendría una velocidad de O(n) (n=7 días).
        """
        self.days_dict[day_button.id]["active"] = day_button.active

    def list_active_day_button(self) -> list:
        """
        Obtiene una lista de estados activos de los días a partir del diccionario days_dict.

        :return: Una lista de booleanos que indican si cada día está activo o no.
        :rtype: list

        Notas:
            - El diccionario self.days_dict se actualiza cada vez que se toca un botón de día.
            - El diccionario contiene claves como 'sunday', 'monday', etc., con valores que son diccionarios.
            - Cada valor del diccionario tiene una clave 'active' que indica si el día está activo.

        Ejemplo:
            Si self.days_dict es:
            {
                'sunday': {'active': True},
                'monday': {'active': False},
                'tuesday': {'active': True},
                'wednesday': {'active': False},
                'thursday': {'active': True},
                'friday': {'active': False},
                'saturday': {'active': True}
            }

            La función devolverá: [True, False, True, False, True, False, True]
        """
        lista_days = list()

        for day, info in self.days_dict.items():
            lista_days.append(info["active"])

        return lista_days


class DayButton(MDIconButton):
    active = BooleanProperty(False)

    def __init__(self, id_num=0, **kwargs):
        """
        Inicializa el DayButton.

        Notas:
            - Los botones siempre inician en estado inactivo (False), por lo que se deja el color inactivo por defecto.
        """
        super(DayButton, self).__init__(**kwargs)
        self.id_num = id_num

    def check_button(self, i, active):
        """
        Cambia el estado activo del botón y actualiza el diccionario de días en el contenedor padre.

        :param i: instancia del botón, no se usa dentro de la función pero se mantiene para compatibilidad.
        :param active: bool, el self.active para saber su estado.
        :return: None

        Notas:
            - la condicion del screen_work es para que solo se pueda modificar si el edit_mode esta en True
            - Cambia el color del botón basado en su nuevo estado activo.
            - Cambia el valor del atributo .active de True a False o viceversa
            - Actualiza el diccionario de días del contenedor padre llamando a `change_list_dicts`.
        """

        screen = MDApp.get_running_app().root.current

        if screen == 'info_task':
            screen_info = MDApp.get_running_app().root.get_screen(screen)

            if screen_info.edit_mode:
                screen_info.apply_changes = True

                self.active = not self.active
                screen_info.tarea.list_days[self.id_num] = self.active
            else:
                SnackbarGeneric(label_text="You must activate edit mode to make changes.",
                                icon="close").open()
            # retorno para evitar que se aplique dos veces el cambio de self.active
            return

        # primero hay que efectuar el cambio del .active y despues editamos el diccionario
        self.active = not self.active
        self.parent.change_list_dicts(self)


        print(self.active)
