

from kivymd.app import MDApp
from kivy.uix.popup import Popup


class PopupEditWork(Popup):
    """
        Popup widget para seleccionar tiempo.
    """

    def __init__(self, **kwargs):
        super(PopupEditWork, self).__init__(**kwargs)

    def on_open(self):
        """
        Notes:
            Se llama al abrirse el PopUp lo cual permite ver la tarea completa
        :return:
        """
        info_screen = MDApp.get_running_app().root.get_screen("info_task")
        self.ids.popup_label_text.text = f"Current Task: {info_screen.tarea.description}"

    def update_label_text(self, text, msg=""):
        """
        Notes:
            Se llama al ingresar una nueva tarea en el popup para mostrar como quedaría la nueva tarea
        :param text: proviene del self.text del MDTextField
        :param msg: es un parametro que pasamos desde el .kv para declarar el mensaje como querramos
        :return:
        """
        self.ids.popup_label_text_new.text += f"{msg}{text}"

    def on_acceptar_pressed(self):
        """
        Notes:
            Se llama al tocar aceptar en el popup lo cual va a actualizar los datos que se muestran en pantalla por
        los nuevos actualizados, a su vez cambia el atributo de info_screen para efectivamente saber que realizamos un
        cambio
        :return:
        """
        if self.ids.input_field.text != "":
            info_screen = MDApp.get_running_app().root.get_screen("info_task")
            info_screen.update_label_tarea_text(self.ids.input_field.text)

        self.dismiss()