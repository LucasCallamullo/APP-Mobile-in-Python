

from kivymd.app import MDApp

class Tarea:
    def __init__(self, description="", hour=0, minute=0, state=False, id=-1,
                 list_days=None, list_repeat=None, soft_delete=False):
        """
        Notes:
            Constructor de mi propia clase para guardar en un objeto mis tareas que voy creando
            cada atributo es bastante referencial pero aclaraciones
            state: se refiere a si ya cumplimos la tarea o no se relacion con list_repeat.
            list_repeat: se refiere a una lista que nos va a contar cuantas veces llevamos haciendo
                o no una tarea en especifico
            list_days: se refiere a una lista para saber si esta activa justo ese día la tarea o no
                en principio almacena [False] * 7 por una razón de cada indice referencia al día
                empezando desde el Lunes, Martes, ..., Domingo
            state_delete: atributo referido al soft_delete ya que si bien es una lista pequeña
                y no tenemos muchas tablas inter-relacionadas, prefiero hacer esta buena practica
                en principio va en False, hasta que eliminemos la tarea.
        """
        self.description = description
        self.hour = hour
        self.minute = minute
        self.state = state
        self.id = id
        self.list_days = [False] * 7 if list_days is None else list_days
        self.list_repeat = [0] if list_repeat is None else list_repeat
        self.soft_delete = soft_delete

    def __str__(self):
        """
        Notes: Es solo una función para poder ver si almacenaba bien mis datos podría borrarla.
        :return: una cadena que es un str directo para usar el print(self)
        """
        cad = "Desc: " + str(self.description)
        cad += "\nID: " + str(self.id)
        cad += "\nState: " + str(self.state)
        cad += "\nHour: " + str(self.hour)
        cad += "\nMinutes: " + str(self.minute)
        cad += "\nList Days: " + str(self.list_days)
        cad += "\nList Repeat: " + str(self.list_repeat)
        cad += "\nSoft Delete: " + str(self.soft_delete)
        cad += "\n=========================="
        return cad

    @classmethod
    def create(cls, list_days=None, desc="", hour=-1, min=-1, edit_mode=False, tarea_obj=None):
        """
        Crea una nueva instancia de la clase `Tarea`.
        Parameters:
        ----------
        cls: class
            Referencia a la clase `Tarea`.
        list_days: list of bool, optional
            Lista de días en los que se repite la tarea. Por defecto es None.
        desc: str, optional
            Descripción de la tarea. Por defecto es una cadena vacía.
        hour: int, optional
            Hora en la que se debe realizar la tarea. Por defecto es -1.
        min: int, optional
            Minuto en el que se debe realizar la tarea. Por defecto es -1.
        edit_mode: bool, optional
            Indica si se está en modo edición. Por defecto es False.
        tarea_obj: Tarea, optional
            Objeto `Tarea` existente que se está editando. Por defecto es None.

        Returns:
        -------
        Tarea or None
            Retorna una nueva instancia de `Tarea` si se cumplen las condiciones necesarias.
            En caso contrario, retorna None.

        Notes:
        -----
        - En modo no edición (`edit_mode`=False), si la descripción está vacía o la hora no está especificada,
          se imprime un mensaje y se retorna None.
        - En modo no edición, si ya existe una tarea con la misma descripción, se imprime un mensaje y se retorna None.
        - En modo no edición, se asigna un nuevo ID a la tarea basado en la longitud de la lista de tareas.
        - En modo edición (`edit_mode`=True), se actualizan los valores de la tarea existente `tarea_obj` con los
          parámetros proporcionados, o se mantienen los valores originales si no se proporcionan nuevos valores.

        Example:
        -------
        # Crear una nueva tarea
        nueva_tarea = Tarea.create(list_days=[True, ..., False, True], desc="Comprar leche", hour=10, min=30)

        # Editar una tarea existente
        tarea_editada = Tarea.create(edit_mode=True, tarea_obj=existing_task, desc="Revisar correo")
        el resto de los params esta dado por lo que pasamos desde tal pantalla
        """

        if not edit_mode:
            if desc == "":
                return None, 0

            if hour == -1:
                return None, 1

            list_tasks = MDApp.get_running_app().list_tasks
            if any(tarea.description == desc for tarea in list_tasks):
                return None, 2

            print(desc)
            id = len(list_tasks)
            list_days = list_days if list_days is not None else [False] * 7

            return cls(description=desc, hour=hour, minute=min, id=id, list_days=list_days), 3

        if edit_mode:
            desc = desc if desc != "" else tarea_obj.description
            hour = hour if hour != -1 else tarea_obj.hour
            min = min if min != -1 else tarea_obj.minute
            id = tarea_obj.id
            list_days = list_days if list_days is not None else [False] * 7

            return cls(description=desc, hour=hour, minute=min, id=id, list_days=list_days), 3
