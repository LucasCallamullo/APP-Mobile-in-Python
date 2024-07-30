

from kivymd.uix.button import MDFillRoundFlatIconButton


class TextIconButton(MDFillRoundFlatIconButton):
    def __init__(self, **kwargs):
        """
        Initializes a custom button with a round flat design and an icon.

        This button is based on MDFillRoundFlatIconButton and can be customized with various properties such as
        text, icon, and color.

        :param kwargs: Additional keyword arguments to customize the button's appearance and behavior.
        """

        super(TextIconButton, self).__init__(**kwargs)

    """ 
        Estas Funciones se llaman en eventos cuando tocan los buttons es por un intento de animación aunque
    podría buscar más al respecto de animaciones pero por ahora messi (se puede bugear el icon)
        Notes:
            No me termino gustando el efecto asique lo saque
from kivy.animation import Animation
from kivymd.uix.behaviors import ScaleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
class TextIconButton(MDFillRoundFlatIconButton, ScaleBehavior, MDBoxLayout):
    def on_release(self):
        self.change_scale_reset(self)

    def on_press(self):
        self.change_scale(self)

    def change_scale(self, instance_button):
        Animation(
            scale_value_x=2,
            scale_value_y=2,
            scale_value_z=2,
            d=0.3,).start(instance_button)

    def change_scale_reset(self, instance_button):
        Animation(
            scale_value_x=1,
            scale_value_y=1,
            scale_value_z=1,
            d=0.3,).start(instance_button)
    """
