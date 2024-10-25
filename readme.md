# 1. Requisitos
- Python 3.8 o superior
- Git
- Visual Studio Code (VS Code) o un editor similar
- Virtualenv para la gestión de entornos virtuales (opcional)
- Acceso al Taiga para la gestion de tareas
# 2. Clonar el Repositorio
- Para empezar, hay que clonar este repositorio en su pc :). En una terminal ejecuta el siguiente comando:
```
git clone https://github.com/superpapus/marieweb.git
```
- Accede al directorio del proyecto:
```
cd marieweb
```
# 3. Instalación de Dependencias
- Puedes crear un entorno virtual en la raíz del proyecto usando:
```
python -m venv venv
```
- Activa el entorno virtual:  
    En Windows:
    ```
    .\venv\Scripts\activate
    ```
- Instala las dependencias:
```
pip install -r requirements.txt
```
# 4. Creación de Ramas y Relación con Taiga
Cada tarea en Taiga tiene un ID único. Para facilitar el orden y seguimiento del progreso usaremos este ID para crear nuestras ramas.
1. Asignación de la tarea en Taiga: Encuentra la tarea que se te asignó en Taiga y toma nota del ID de la tarea (por ejemplo, `#123 Nombre de la tarea`).

2. Creación de la rama en VS Code:
    - Abre el proyecto en VS Code.
    - (Método 1) Abre una terminal y escribe el siguiente comando para crear una nueva rama. Usa el ID de la tarea de Taiga en el nombre:
      ```
      git checkout -b #123-nombre-tarea
      ```
      Nota: Cambiando #123-nombre-tarea por el ID y nombre de la tarea.
    - (Método 2) En el Visual Studio Code abajo a la izquierda, aparecerá el nombre de la rama `dev`, al hacer clic aparecerá un menú con las ramas actuales, selecciona `Create new branch from...` para crear una rama desde.. y selecciona la rama `dev` y a continuación ingresas el nombre de la rama siguiendo el mismo formato mencionado anteriormente `#123-nombre-tarea`.
    - Cambio de rama: Ahora estarás en la nueva rama y podrás comenzar a trabajar en los cambios necesarios para esta tarea.

# 5. Commit y Push
1. Preparación del Commit:
    - Asegúrate de haber probado el código y que todo funciona correctamente.
    - Añade los archivos modificados:
    ```
    git add .
    ```
2. Realización del Commit:
    - Escribe un mensaje que resuma los cambios realizados en el commit, incluyendo el ID de la tarea:
    ```
    git commit -m "Añadir [Funcion/Corrección] para tarea #123"
    ```
3. Push de la Rama:
    - Envía los cambios a GitHub en tu rama actual:
    ```
    git push origin #123-nombre-tarea
    ```
# 6. Pull Requests y Flujo de Revisión
Para integrar los cambios a la rama principal de desarrollo (`dev`), hay que crear una Pull Request (PR):

1. Creación del Pull Request:
    - En GitHub, ve a la sección de "Pull requests".
    - Haz clic en "New pull request" y selecciona la rama `dev` como base y tu rama como comparación.
    - Ingresa un nombre descriptivo al PR y escribe una breve descripción de los cambios realizados y el ID de la tarea.
    - Asigna revisores si es necesario y asegura de que el PR esté listo para revisión.
2. Revisión y Fusión:
    - Una vez aprobado, un revisor o tú mismo podrás hacer "Merge" a `dev`.
    - Elimina la rama en GitHub después del "Merge" si ya no es necesaria. <3