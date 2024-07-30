

from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarCloseButton, MDSnackbarActionButton


class SnackbarGeneric(MDSnackbar):
    def __init__(self, label_text="", button_text="", icon=None, icon_color="red", **kwargs):
        """
        Initializes a generic snackbar with optional label text, button text, and icon.

        :param label_text: str, The main text to display on the snackbar.
        :param button_text: str, The text for the action button (optional).
        :param icon: str, The icon to display on the snackbar (optional).
        :param icon_color: str, The color of the icon (default is "red").
        :param kwargs: Additional keyword arguments for the MDSnackbar.

        Notes:
            - If `button_text` is provided, an action button is added to the snackbar.
            - If `icon` is provided, a close button with the specified icon is added to the snackbar.
        """
        super(SnackbarGeneric, self).__init__(**kwargs)

        # Add a label with the specified text to the snackbar
        self.add_widget(MDLabel(
                text=label_text
        ))

        # Add an action button if `button_text` is provided
        if button_text != "":
            self.add_widget(MDSnackbarActionButton(
                    text=button_text,
                    theme_text_color="Custom",
                    text_color="#8E353C"
            ))

        # Add a close button with an icon if `icon` is provided
        if icon is not None:
            self.add_widget(MDSnackbarCloseButton(
                    icon=icon,
                    theme_text_color="Custom",
                    text_color=icon_color,
                    on_press=self.action_callback    # Set the callback function for the button press
                ))

    def action_callback(self, instance):
        """
        Callback function for the close button action.

        :param instance: The instance of the button that triggered the callback.

        Notes:
            - Dismisses the snackbar when the close button is pressed.
        """
        self.dismiss()

