

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

# Bibliotecas extra
import datetime
from datetime import date
from math import ceil, floor, exp

from kivymd.uix.list import MDList

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty, AliasProperty, ObjectProperty, StringProperty




class ListTodoCard(MDList):
    """ realmente no se si es necesario probable de borrar. """

    def __init__(self, **kwargs):
        super(ListTodoCard, self).__init__(**kwargs)

        self.bind(minimum_height=self.setter('height'))
        self.widgets_dict = {}  # Diccionario para indexar widgets


class MainScreen(MDScreen):
    """
        Pantalla principal de la aplicación, muestra la lista de tareas y la fecha.
    """
    # current = StringProperty(None)

    def __init__(self, **kwargs):
        """
        Notes:
            Agregamos simplemente un atributo para poder usarlo en la función on_start de la app
        :param kwargs:
        """
        super(MainScreen, self).__init__(**kwargs)
        self.today_id = 0

    def on_enter(self):
        """
        Notes:
            Se ejecuta cada vez que se muestra la pantalla. Actualiza la fecha actual.
        """
        today = date.today()
        # wd = date.weekday(today)
        self.today_id = date.weekday(today)
        days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        self.ids.date.text = f"{days[self.today_id]}, {day} {month} {year}"

    def add_widget_in_todo_list(self, task_to_add):
        """
        :param
        :return:
        """
        todo_list_widget = self.ids.todo_list
        todo_list_widget.add_widget(task_to_add)
        todo_list_widget.widgets_dict[task_to_add.tarea.id] = task_to_add

    def update_widget_in_todo_list(self, task_update):

        todo_list_widget = self.ids.todo_list

        widget = todo_list_widget.widgets_dict.get(task_update.id)

        if widget:
            widget.tarea = task_update

            # llamo al metodo de TareaCard para actualizar los titulos
            widget.update_texts_on_label()

            # Reasigna el widget actualizado al diccionario (opcional, no es realmente necesario)
            # Ya que los diccionarios a hacer referencia al objeto cualquier cambio efectuado se verá reflejado
            # directamente.
            todo_list_widget.widgets_dict[task_update.id] = widget

            # llamo al metodo de TareaCard para sobreescribir el archivo de memoria binario
            widget.save_write_data()

            print("mi widget_tarea:")
            print(widget.tarea)

        """ 
        este era la anterior logica pero fue cambiado ya que al ser una busqeuda secuencial con complejidad
        O(n) era mucho mas lenta que la complejidad de los diccionarios de aproximadamente O(1)
        for child in self.ids.todo_list.children:
            if hasattr(child, 'tarea') and child.tarea.id == task_update.id:
                # Actualiza los atributos del widget directamente
                child.tarea = task_update
                # Llama al método para actualizar sus datos de visualización
                child.update_texts_on_label()
                break
        """

    def remove_widget_from_todo_list(self, task_delete):
        """
        Elimina el widget de la lista de tareas correspondiente al ID de la tarea.

        Parameters:
        ----------
        task_id : int
            El ID de la tarea que se desea eliminar.
        """


        todo_list_widget = self.ids.todo_list


        widget = todo_list_widget.widgets_dict.get(task_delete.id)

        if widget:
            # llamo al metodo de TareaCard para sobreescribir el archivo de memoria binario para que quede
            # guardado el nuevo estado de soft delete
            widget.tarea = task_delete
            widget.save_write_data()

            todo_list_widget.remove_widget(widget)

            # esto lo elimina del diccionario por ahora no es lo que quiero
            del todo_list_widget.widgets_dict[task_delete.id]


class RouletteScrollEffect(ScrollEffect):
    __events__ = ('on_coasted_to_stop',)

    drag_threshold = NumericProperty(0)
    '''overrides :attr:`ScrollEffect.drag_threshold` to abolish drag threshold.

    .. note::
        If using this with a :class:`Roulette` or other :class:`Tickline`
        subclasses, what matters is :attr:`Tickline.drag_threshold`, which
        is passed to this attribute in the end.
    '''

    min = NumericProperty(-float('inf'))
    max = NumericProperty(float('inf'))

    # interval = NumericProperty(50)
    interval = NumericProperty(10)
    '''the interval of the values of the "roulette".'''

    anchor = NumericProperty(0)
    '''one of the valid stopping values.'''

    pull_duration = NumericProperty(.2)
    '''when movement slows around a stopping value, an animation is used
    to pull it toward the nearest value. :attr:`pull_duration` is the duration
    used for such an animation.'''

    coasting_alpha = NumericProperty(.5)
    '''When within :attr:`coasting_alpha` * :attr:`interval` of the
    next notch and velocity is below :attr:`terminal_velocity`, 
    coasting begins and will end on the next notch.'''

    pull_back_velocity = NumericProperty('50sp')
    '''the velocity below which the scroll value will be drawn to the 
    *nearest* notch instead of the *next* notch in the direction travelled.'''

    _anim = ObjectProperty(None)

    def get_term_vel(self):
        return (exp(self.friction) * self.interval *
                self.coasting_alpha / self.pull_duration)

    def set_term_vel(self, val):
        self.pull_duration = (exp(self.friction) * self.interval *
                              self.coasting_alpha / val)

    terminal_velocity = AliasProperty(get_term_vel, set_term_vel,
                                      bind=['interval',
                                            'coasting_alpha',
                                            'pull_duration',
                                            'friction'],
                                      cache=True)
    '''if velocity falls between :attr:`pull_back_velocity` and 
    :attr:`terminal velocity` then the movement will start to coast
    to the next coming stopping value.

    :attr:`terminal_velocity` is computed from a set formula given
    :attr:`interval`, :attr:`coasting_alpha`, :attr:`pull_duration`,
    and :attr:`friction`. Setting :attr:`terminal_velocity` has the
    effect of setting :attr:`pull_duration`.
    '''

    def start(self, val, t=None):
        if self._anim:
            self._anim.stop(self)
        return ScrollEffect.start(self, val, t=t)

    def on_notch(self, *args):
        return (self.scroll - self.anchor) % self.interval == 0

    def nearest_notch(self, *args):
        interval = float(self.interval)
        anchor = self.anchor
        n = round((self.scroll - anchor) / interval)
        return anchor + n * interval

    def next_notch(self, *args):
        interval = float(self.interval)
        anchor = self.anchor
        round_ = ceil if self.velocity > 0 else floor
        n = round_((self.scroll - anchor) / interval)
        return anchor + n * interval

    def near_notch(self, d=0.01):
        nearest = self.nearest_notch()
        if abs((nearest - self.scroll) / self.interval) % 1 < d:
            return nearest
        else:
            return None

    def near_next_notch(self, d=None):
        d = d or self.coasting_alpha
        next_ = self.next_notch()
        if abs((next_ - self.scroll) / self.interval) % 1 < d:
            return next_
        else:
            return None

    def update_velocity(self, dt):
        if self.is_manual:
            return
        velocity = self.velocity
        t_velocity = self.terminal_velocity
        next_ = self.near_next_notch()
        pull_back_velocity = self.pull_back_velocity
        if pull_back_velocity < abs(velocity) < t_velocity and next_:
            duration = abs((next_ - self.scroll) / self.velocity)
            anim = Animation(scroll=next_,
                             duration=duration,
                             )
            self._anim = anim
            anim.on_complete = self._coasted_to_stop
            anim.start(self)
            return
        if abs(velocity) < pull_back_velocity and not self.on_notch():
            anim = Animation(scroll=self.nearest_notch(),
                             duration=self.pull_duration,
                             t='in_out_circ')
            self._anim = anim
            anim.on_complete = self._coasted_to_stop
            anim.start(self)
        else:
            self.velocity -= self.velocity * self.friction
            self.apply_distance(self.velocity * dt)
            self.trigger_velocity_update()

    def on_coasted_to_stop(self, *args):
        """
        this event fires when the roulette has stopped, "making a selection".
        """
        pass

    def _coasted_to_stop(self, *args):
        self.velocity = 0
        self.dispatch('on_coasted_to_stop')


class ScrollViewTodoCard(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollViewTodoCard, self).__init__(**kwargs)
        self.effect_y = RouletteScrollEffect(anchor=20, interval=80)
