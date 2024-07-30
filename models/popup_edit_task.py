

from kivymd.app import MDApp
from kivy.uix.popup import Popup


class PopupEditWork(Popup):
    """
    Popup widget for editing a task.
    """

    def __init__(self, **kwargs):
        """
        Initializes the PopupEditWork instance.
        """
        super(PopupEditWork, self).__init__(**kwargs)

    def to_dismiss(self):

        self.ids.popup_label_text_new.text = ""
        self.ids.input_field.text = ""

        self.ids.input_field.icon_right = "note-alert-outline"

        self.dismiss()

    def on_open(self):
        """
        Called when the popup is opened. Displays the current task description.

        Notes:
            This method is triggered when the popup opens, allowing the user to see the complete task.
        """
        info_screen = MDApp.get_running_app().root.get_screen("info_task")
        self.ids.popup_label_text.text = f"Current Task: {info_screen.tarea.description}"

    def update_label_text(self, text, msg=""):
        """
        Updates the label text in the popup to show the new task description.

        Notes:
            This method is called when a new task is entered in the popup to show how the new task will look.

        :param text: The new task description from the MDTextField.
        :param msg: A custom message passed from the .kv file to prepend to the text.
        """
        self.ids.popup_label_text_new.text += f"{msg}{text}"

    def on_accept_pressed(self):
        """
        Updates the task description and closes the popup when the accept button is pressed.

        Notes:
            This method updates the displayed task data with the new description into in the popup.
            It also changes the attribute in info_screen to indicate that a change was made.

        """
        if self.ids.input_field.text != "":
            info_screen = MDApp.get_running_app().root.get_screen("info_task")
            info_screen.update_label_tarea_text(self.ids.input_field.text)

        # self.dismiss()
        self.to_dismiss()
