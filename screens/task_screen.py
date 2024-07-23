

from kivymd.uix.screen import MDScreen

from models.popup_time_select import *
from models.day_button import *
from models.tarea import *
from models.tarea_card import *

from models.snackbar_generic import *


class AddTaskScreen(MDScreen):

    def __init__(self, **kwargs):
        """
        Constructor de la clase AddTaskScreen.

        Notes:
            popup crea al popup select time, como un objeto dentro de la screen para llamarlo cuando querramos
            description(str): hace referencia al valor que ingresamos como texto. inicia vacío para ser bandera
            hours_value(int): es la hora recuperada del popup, empieza en -1 para ser bandera

        """
        super(AddTaskScreen, self).__init__(**kwargs)
        self.popup = PopupSelectTime()

        self.description = ""
        self.hours_value = -1
        self.minutes_value = 0

        self.tarea = None
        self.id_text_snackbar = ""

    def on_enter(self):
        self.add_widget(GridButtonsDay())

    def on_leave(self, *args):
        self.ids.display_work.text = ""
        self.ids.display_time.text = ""

    # =================================================================
    #       Updates Labels Texts.
    # =================================================================
    def reset_text_labels(self, text_task="", text_time=""):
        self.ids.display_work.text = text_task
        self.ids.display_time.text = text_time
        self.ids.input_field.text = ""

    def update_label_text(self, description):
        """
            Actualiza el MDLabel que muestra la tarea y nos muestra el nuevo texto que ingresamos.
        """
        self.description = description.strip().capitalize()
        self.ids.display_work.text += f"{self.description}"

    def update_label_hour(self, hours_value, minutes_value):
        self.hours_value = int(hours_value)
        self.minutes_value = int(minutes_value)
        self.ids.display_time.text += f"{self.hours_value:02d}:{self.minutes_value:02d}"

    # =================================================================
    #       Buttons Actions of Task Screen
    # =================================================================
    def add_todo(self):
        """
            Notes:
                Se llama desde (work_screen: button_aceptar) lo que hace es llamar Tarea.create() y nos devuelva
                si se pudo crear la tarea a partir de los datos completados en los distintos labels de add_work
                si se creó devuelve una Tarea=Objeto completo, si no devuelve None

                En caso de que se cree agrega un widget de TodoCard() al (main_screen: id:todo_list)

            =======================================================================================================
                esta forma si bien funciona podría ser un problema si yo quisiera hacer un reset de los datos al
                salir de add_work revisar, podría crear la propia clase tarea en work_screen como atributo y mandarlo
                como atributo
            =======================================================================================================
        """
        list_days = self.ids.grid_buttons.list_active_day_button()
        self.tarea, self.id_text_snackbar = Tarea.create(list_days=list_days, desc=self.description,
                                                      hour=self.hours_value, min=self.minutes_value)

        if self.tarea:
            main_screen = MDApp.get_running_app().root.get_screen("main")
            main_screen.ids.todo_list.add_widget(TareaCard(self.tarea))

    def switch_navigation(self):
        """
        Notes:
             Simplemente es una forma de volver directo al switch_tab "main_tab" ya que no se puede volver
             directo al screen "main" debido al bottom_navigation
        """
        main_screen = MDApp.get_running_app().root.get_screen("main")
        main_screen.ids.bottom_nav.switch_tab("main_tab")
