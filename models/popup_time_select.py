

from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout


class PopupSelectTime(Popup):
    """
        Popup widget for selecting time.
    """
    def __init__(self, **kwargs):
        super(PopupSelectTime, self).__init__(**kwargs)

    def on_acceptar_pressed(self):
        """
        - Method invoked when the 'Accept' button is pressed in the time selection popup.
        - Obtains the selected hour and minute values from the UI widgets.
        - Updates the current screen depending on whether it is 'main' or 'info_work', using the selected
        hour and minute values.

        Notes:
            - If the current screen is 'main', updates the 'add_work' widget with the time values.
            - If the current screen is 'info_task', calls the 'update_label_hour' method directly on the
              'info_task' screen to update the values.
        """

        hours_value = self.ids.hour_time.current_num    # int
        minutes_value = self.ids.min_time.current_num   # int

        # Get the current screen where the popup is located and then sends it to its respective
        # functions within each screen as appropriate.
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
        Widget for selecting numbers using touch sliding.
    """
    current_num = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(23)

    def on_touch_move(self, touch):
        """
            Handles touch movement to increment or decrement the number.

            Parameters:
            ----------
            touch : MotionEvent
                Touch event object.
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
            Increments or decrements the current number within the specified range.

            Parameters:
            ----------
            value : int
                Value to increment or decrement the number.
        """
        self.current_num = (self.current_num + value) % (self.max_value + 1)
