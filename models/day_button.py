

from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.color_definitions import colors

from kivy.properties import BooleanProperty     # , ListProperty

from models.snackbar_generic import SnackbarGeneric


class GridButtonsDay(MDGridLayout):
    """
        * It might still be possible to improve the creation of the dictionary to use 7 iterations instead of 14,
          but for now, I'll leave it as is.
        * I should also consider how to pass a list of icon names as a parameter from the .kv file
          to use in this constructor. Although I think it should be passed through the work screen first—I'll check.
    """
    def __init__(self, lista_active=None, **kwargs):
        """
        Constructor for GridButtonsDay.

        This constructor initializes a dictionary to facilitate the generic creation of buttons
        for each day of the week. The buttons are added to the layout at the time of object creation.

        Notes:
            - A dictionary is used to store the state, icon, and ID of each day.

        Parameters:
            **kwargs: Keyword arguments for initialization.
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
        Updates the day dictionary with the current state of the day button.

        :param day_button: The day button whose information is being updated.
        :type day_button: DayButton()
        :return: None
        Notes:
            A dictionary is used to access the day state directly with O(1) speed,
            instead of iterating through a list, which would have O(n) speed (n=7 days).
        """
        # Check if the ID of the day button is in the dictionary
        self.days_dict[day_button.id]["active"] = day_button.active

    def list_active_day_button(self) -> list:
        """
        Retrieves a list of active states of the days from the days_dict dictionary.

        :return: A list of booleans indicating whether each day is active or not.
        :rtype: list

        Notes:
            - The self.days_dict dictionary is updated every time a day button is pressed.
            - The dictionary contains keys such as 'sunday', 'monday', etc., with values that are dictionaries.
            - Each dictionary value has a key 'active' indicating if the day is active.

        Example:
            If self.days_dict is:
            {
                'sunday': {'active': True},
                'monday': {'active': False},
                'tuesday': {'active': True},
                'wednesday': {'active': False},
                'thursday': {'active': True},
                'friday': {'active': False},
                'saturday': {'active': True}
            }

            The function will return: [True, False, True, False, True, False, True]
        """
        lista_days = list()

        for day, info in self.days_dict.items():
            lista_days.append(info["active"])

        return lista_days

    def reset_days_buttons(self):
        """
        Resets the state of all DayButton widgets within the GridButtonsDay layout.

        This method iterates through all child widgets of the GridButtonsDay layout,
        identifies those that are instances of DayButton, and resets their state.

        The following updates are made to each DayButton:
            - `active` attribute is set to False, indicating that the button is not active.
            - `md_bg_color` attribute is updated to a gray color, representing the inactive state.

        This method is typically used to reset the appearance and state of day buttons
        when transitioning away from a tab screen or performing a similar reset action.

        Notes:
            - The color for inactive buttons is set using the `colors` dictionary with the key "BlueGray" and the value "600".
        """
        for child in self.children:
            if isinstance(child, DayButton):
                child.active = False
                child.md_bg_color = colors["BlueGray"]["600"]  # Actualiza el color según el estado
                self.change_list_dicts(child)


class DayButton(MDIconButton):
    active = BooleanProperty(False)

    def __init__(self, id_num=0, **kwargs):
        """
        Initializes the DayButton.

        Notes:
            - The buttons always start in inactive (False) state, so the inactive color is set by default.
            - The `id_num` parameter represents the numeric identifier for the button. It is used for
            indexing or identification purposes.

        Parameters:
            id_num (int): Numeric identifier for the button. Default is 0.
            **kwargs: Additional keyword arguments for initialization.
        """
        super(DayButton, self).__init__(**kwargs)
        self.id_num = id_num

    def check_button(self, i, active):
        """
        Changes the active state of the button and updates the parent container's days dictionary.

        :param i: Instance of the button. Although it is not used within the function, it is kept
        for compatibility.
        :param active: bool, the `self.active` state of the button to know its state.
        :return: None

        Notes:
            - The condition checking `screen_work` is to ensure modifications can only be made
            if `edit_mode` is True.
            - Changes the button color based on its new active state.
            - Toggles the value of the `self.active` attribute between True and False.
            - Updates the parent container's days dictionary by calling `change_list_dicts`.
        """

        screen = MDApp.get_running_app().root.current

        if screen == 'info_task':
            screen_info = MDApp.get_running_app().root.get_screen(screen)

            if screen_info.edit_mode:
                screen_info.apply_changes = True

                self.active = not self.active
                screen_info.tarea.list_days[self.id_num] = self.active

                # First, toggle the .active state, then update the dictionary
                self.parent.change_list_dicts(self)

            else:
                SnackbarGeneric(label_text="You must activate edit mode to make changes.",
                                icon="close").open()
            # Return to prevent the change to `self.active` from being applied twice
            return

        # First, toggle the .active state, then update the dictionary
        self.active = not self.active
        self.parent.change_list_dicts(self)

        # print(f"estado del botm: {self.active}")
