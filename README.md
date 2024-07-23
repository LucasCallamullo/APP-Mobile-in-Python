# APP-Mobile-in-Python
Python + KivyMD for a app mobile.

[EN]

Python 3.12: The project is developed using Python 3.12, ensuring compatibility with the latest features and improvements of the language.

Kivy: A framework for developing multi-touch applications, used to build the application's graphical user interface (GUI).

KivyMD 1.2.0: A library providing Material Design components for Kivy, enhancing the visual design and functionality of the application.

Custom Design: The design is tailored to the specific needs of the application. While it adheres to good frontend development practices, there is room for further improvement.

Modularity: The project demonstrates good modularization practices by separating design (frontend) and functionality (backend) into distinct components.

Data Storage: Data is saved using Python's pickle module, which allows for serialization of data into binary files.

Data Retrieval: Data is loaded from binary files using the pickle module, enabling the restoration of saved tasks.

Task Object: The Task object represents tasks that can be created, edited, saved, and deleted. It is stored as a binary file and can be retrieved when needed.

Soft Delete: Implemented to avoid permanent loss of tasks. Soft delete marks tasks as deleted without actually removing them from the list.

Unique IDs: The application uses unique IDs corresponding to indices in the list, ensuring proper management and retrieval of tasks.

Module Optimization: Modules are optimized for efficiency, with methods and functions organized systematically according to their respective files.

Mathematical Logic: Mathematical logic is applied to solve various functions, improving the functionality and performance of the application.

File Structure:

models/: Contains the models used in the application.
kv/: Contains Kivy language files (KV), similar to CSS but for designing the user interface.
screens/: Contains the different screens of the application, defining the design and functionality of each page.
main.py: Contains the file to run the .py code.
Flexibility:

Adaptability to Databases: The core logic for managing tasks can be adapted to work with various database systems. While the application is designed to use binary files, similar principles apply to using databases: storing, retrieving, and manipulating tasks follows a similar logic.
Object-Oriented Programming (OOP)
The project utilizes Object-Oriented Programming (OOP) principles to structure and organize code effectively. Key classes such as TareaCard, GridButtonsDay, and DayButton encapsulate data and functionality, enhancing modularity and readability. This approach simplifies code maintenance and supports scalability.
Future improvements might involve refining class hierarchies or using design patterns to address specific needs more efficiently.

Use of Dictionaries
Dictionaries are extensively used to manage and access data efficiently. For example, the GridButtonsDay class employs a dictionary (days_dict) to store and retrieve button states, icons, and IDs. This design choice optimizes data access with O(1) complexity, making the code more efficient compared to linear searches.

List Comprehensions
List comprehensions are used for concise and readable data manipulation. For instance, when initializing the lista_active attribute, a list comprehension is used to generate a default list of False values for each day of the week. This approach simplifies the code and enhances readability.

Data Management
The project leverages the pickle module for binary data storage and retrieval. This choice enables efficient serialization of Task objects into binary files and their subsequent restoration. Using binary files helps preserve data integrity and supports seamless data management.

User Interface (UI) Design
The use of KivyMD and KV language provides a flexible and dynamic UI design. Although the current design meets the application's requirements, there is potential for further refinement to enhance user experience and visual appeal.

Additional Considerations
Error Handling: Robust error handling mechanisms are implemented to ensure smooth operation and a good user experience.
Performance Optimization: The application is optimized for performance, with efficient data access and manipulation techniques.
Documentation: Comprehensive documentation is provided in both English and Spanish, ensuring accessibility for a wider audience.

=================================================================================================================================

[ES]

Características del Proyecto
Python 3.12: El proyecto está desarrollado utilizando Python 3.12, asegurando compatibilidad con las últimas características y mejoras del lenguaje.

Kivy: Es un framework para el desarrollo de aplicaciones multi-táctiles, utilizado para construir la interfaz gráfica de usuario (GUI) de la aplicación.

KivyMD 1.2.0: Es una biblioteca que proporciona componentes de Material Design para Kivy, mejorando el diseño visual y la funcionalidad de la aplicación.

Diseño Personalizado: El diseño está adaptado a las necesidades específicas de la aplicación. Aunque sigue buenas prácticas para el desarrollo del frontend, hay margen para mejoras adicionales.

Modularización: El proyecto muestra buenas prácticas de modularización al separar el diseño (frontend) y la funcionalidad (backend) en componentes distintos.

Almacenamiento de Datos: Los datos se guardan utilizando el módulo pickle de Python, que permite la serialización de datos en archivos binarios.

Recuperación de Datos: Los datos se cargan desde archivos binarios utilizando el módulo pickle, lo que permite la restauración de tareas guardadas.

Objeto Tarea: El objeto Task representa las tareas que se pueden crear, editar, guardar y eliminar. Se almacena como un archivo binario y puede recuperarse cuando sea necesario.

Eliminación Suave (Soft Delete): Implementada para evitar la pérdida permanente de tareas. La eliminación suave marca las tareas como eliminadas sin realmente removerlas de la lista.

IDs Únicos: La aplicación utiliza IDs únicos que corresponden a los índices en la lista, asegurando una gestión y recuperación adecuada de las tareas.

Optimización de Módulos: Los módulos están optimizados para la eficiencia, con métodos y funciones organizados de manera ordenada según sus respectivos archivos.

Lógica Matemática: Se aplica lógica matemática para la resolución de diversas funciones, mejorando la funcionalidad y el rendimiento de la aplicación.

Estructura de Archivos:

models/: Contiene los modelos utilizados en la aplicación.
kv/: Contiene archivos de lenguaje Kivy (KV), que son similares al CSS pero para diseñar la interfaz de usuario.
screens/: Contiene las diferentes pantallas de la aplicación, definiendo el diseño y la funcionalidad de cada página.
main.py: Contiene el archivo para correr el .py

Flexibilidad:
Adaptabilidad a Bases de Datos, La lógica central para gestionar tareas puede adaptarse para trabajar con varios sistemas de bases de datos. Aunque la aplicación está diseñada para usar archivos binarios, los principios similares se aplican al usar bases de datos: almacenar, recuperar y manipular tareas sigue una lógica similar.

Programación Orientada a Objetos (OOP)
El proyecto utiliza principios de Programación Orientada a Objetos (OOP) para estructurar y organizar el código de manera efectiva. Clases clave como TareaCard, GridButtonsDay y DayButton encapsulan datos y funcionalidades, mejorando la modularidad y la legibilidad. Este enfoque simplifica el mantenimiento del código y soporta la escalabilidad.
Las futuras mejoras podrían implicar refinar las jerarquías de clases o utilizar patrones de diseño para abordar necesidades específicas de manera más eficiente.

Uso de Diccionarios
Se utilizan diccionarios extensamente para gestionar y acceder a los datos de manera eficiente. Por ejemplo, la clase GridButtonsDay emplea un diccionario (days_dict) para almacenar y recuperar estados de botones, íconos e IDs. Esta elección de diseño optimiza el acceso a los datos con una complejidad de O(1), haciendo el código más eficiente en comparación con búsquedas lineales.

Listas por Comprensión
Se utilizan listas por comprensión para la manipulación concisa y legible de datos. Por ejemplo, al inicializar el atributo lista_active, se utiliza una lista por comprensión para generar una lista predeterminada de valores False para cada día de la semana. Este enfoque simplifica el código y mejora la legibilidad.

Gestión de Datos
El proyecto utiliza el módulo pickle para el almacenamiento y la recuperación de datos en formato binario. Esta elección permite la serialización eficiente de objetos de tarea (Tarea) en archivos binarios y su posterior restauración. El uso de archivos binarios ayuda a preservar la integridad de los datos y soporta una gestión de datos sin problemas.

Diseño de la Interfaz de Usuario (UI)
El uso de KivyMD y el lenguaje KV proporciona un diseño de interfaz flexible y dinámico. Aunque el diseño actual cumple con los requisitos de la aplicación, hay potencial para una mayor refinación para mejorar la experiencia del usuario y el atractivo visual.

Consideraciones Adicionales
Manejo de Errores: Se implementan mecanismos robustos de manejo de errores para garantizar un funcionamiento fluido y una buena experiencia de usuario.
Optimización del Rendimiento: La aplicación está optimizada para el rendimiento, con técnicas eficientes de acceso y manipulación de datos.
Documentación: Se proporciona una documentación completa en inglés y español, asegurando accesibilidad para una audiencia más amplia.
