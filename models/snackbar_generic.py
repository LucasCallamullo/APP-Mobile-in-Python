

from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarCloseButton, MDSnackbarActionButton


class SnackbarGeneric(MDSnackbar):
    def __init__(self, label_text="", button_text="", icon=None, icon_color="red", **kwargs):
        """

        """
        super(SnackbarGeneric, self).__init__(**kwargs)

        self.add_widget(MDLabel(
                text=label_text
        ))

        if button_text != "":
            self.add_widget(MDSnackbarActionButton(
                    text=button_text,
                    theme_text_color="Custom",
                    text_color="#8E353C"
            ))

        if icon is not None:
            self.add_widget(MDSnackbarCloseButton(
                    icon=icon,
                    theme_text_color="Custom",
                    text_color=icon_color,
                    on_press=self.action_callback
                ))

    def action_callback(self, instance):
        self.dismiss()

