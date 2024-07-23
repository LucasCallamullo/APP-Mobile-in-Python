

from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout


class PopupSelectTime(Popup):
    """
        Popup widget para seleccionar tiempo.
    """
    def __init__(self, **kwargs):
        super(PopupSelectTime, self).__init__(**kwargs)

    def on_acceptar_pressed(self):
        """
        Método invocado cuando se presiona el botón 'Aceptar' en el popup de selección de tiempo.

        Obtiene los valores de horas y minutos seleccionados desde los widgets de la interfaz de usuario.
        Actualiza la pantalla actual dependiendo de si es 'main' o 'info_work', utilizando los valores
        de horas y minutos seleccionados.

        Notes:
            - Si la pantalla actual es 'main', se actualiza el widget 'add_work' con los valores de tiempo.
            - Si la pantalla actual es 'info_work', se llama al método 'update_label_hour' directamente
              en la pantalla 'info_work' para actualizar los valores y se establece 'apply_changes' en True.
        """
        hours_value = self.ids.hour_time.current_num    # int
        minutes_value = self.ids.min_time.current_num   # int

        # lo que hago es obtener la pantalla actual en la que se encuentra el popup
        # y luego lo mando a sus funciones dentro de cada script según corresponda
        actual_screen = MDApp.get_running_app().root.current
        screen = MDApp.get_running_app().root.get_screen(actual_screen)

        if actual_screen == "main":
            screen.ids.add_work.update_label_hour(hours_value, minutes_value)

        elif actual_screen == "info_task":
            screen.update_label_hour(hours_value, minutes_value)

        self.dismiss()


#   ==========================================================================
#                       HOW TO CREATE ON TOUCH LABEL
#   ==========================================================================
class NumberSelector(BoxLayout):
    """
        Widget para seleccionar números con deslizamiento táctil.
    """
    current_num = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(23)

    def on_touch_move(self, touch):
        """
            Maneja el movimiento táctil para incrementar o decrementar el número.

            Parameters:
            ----------
            touch : MotionEvent
                Objeto de evento táctil.
        """

        if self.collide_point(*touch.pos):
            if touch.dy > 5:  # Sensibilidad al deslizamiento hacia arriba
                self.increment_num(1)
                touch.ud['handled'] = True
            elif touch.dy < -5:  # Sensibilidad al deslizamiento hacia abajo
                self.increment_num(-1)
                touch.ud['handled'] = True

    def increment_num(self, value):
        """
            Incrementa o decrementa el número actual dentro del rango especificado.

            Parameters:
            ----------
            value : int
                Valor para incrementar o decrementar el número.
        """
        self.current_num = (self.current_num + value) % (self.max_value + 1)