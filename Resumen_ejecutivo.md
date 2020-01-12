#### Resumen Ejecutuvo

El objetivo de este proyecto es ampliar la funcionalidad de un proyecto educativo llamado decide, que consiste en una plataforma de voto electrónico. Este proyecto tiene el fin de poder acercar al alumno a trabajar con proyecto que se podrán encontrar en un futuro cercano cuando desempeñe su actividad laboral, así como tratar de enseñar al alumno los métodos básicos de gestión de incidencias y código fuente que se llevan a cabo durante un proyecto software. Para más información acerca del proyecto Decide consulte la siguiente página: https://github.com/decide-moltres/decide

### Alcance del proyecto

Para llevar a cabo este aprendizaje en concreto se nos ha asignado uno de los submódulos que forma Decide.
En concreto en este grupo hemos desarrollado en módulo de votación implementado, funcionalidad que se exigía en el pliego de la asignatura, así como funcionalidad extra que nos han pedido otros grupos que tenían otros submódulos de Decide, que deseaban hacer operaciones con el submódulo voting. Esta funcionalidad se caracteriza por implementar las elecciones de primarias, senado y presidenciales, así como ofrecer una API Rest de Voting y Political Parties para que el resto e los módulos puedan usar toda la información a través de la consulta de una url.

### Tecnologías empleadas

En proyecto se ha seguido desarrollándose en las tecnologías en los que fueron creados en un principio, por lo que para el desarrollo hemos continuado usando Python en su versión 3.6, en el framework Django, y como base de datos hemos usado Postgres. También hemos empleado otras tecnologías como Travis, Heroku, Codacy, que se explican en el apartado tattal


## Indicadores del proyecto



Miembro del equipo  | Horas | Commits | LoC | Test | Issues | Incremento |
------------- | ------------- | ------------- | ------------- | ------------- | ------------- |  ------------- | 
[Pérez Barrera, Juan Luis](https://github.com/juanluisperez1) | -- | 10 | ZZ | 6 | 7 | Creación API Political Party 
[Aguza Barragán, Jose Manuel](https://github.com/Aguza5) | -- | 27 | YY | 5 | 14 | Creación de las Primary Elections 
[Ripoll Torejón, Pablo](https://github.com/PabloRT98) | -- | 24 | YY | ZZ | 10 | Creación de las Senate Elections 
[García Limones, Raúl](https://github.com/raugarlim) | -- | 19 | YY | 5 | 9 | Creación de las Presidenciales Elections y métedo de API de voting 
[Castro Cachero, Álvaro Juan](https://github.com/alvcascac) | -- | 7 | YY | 4 | 9 | Tipo de votación other, que incluyes repuestas yes/no auto generadas
**TOTAL** | --  | 90 | tYY | 20 | 49 | Implementación de las votaciones estipuladas en el pliego, añadiendo también una API para accerder a las votaciones 

  _**Anotación** en este apartado no hemos incluido las horas que cada miembro ha invertido en el proyecto puesto que consideramos que todos los miembros del equipo hemos invertido la misma cantidad de tiempo en cada una de las tareas que teniamos asignadas_
  
La tabla contiene la información de cada miembro del proyecto y el total de la siguiente forma: 
  * Commits: solo contar los commits hechos por miembros del equipo, no lo commits previos
  * LoC (líneas de código): solo contar las líneas producidas por el equipo y no las que ya existían o las que se producen al incluir código de terceros
  * Test: solo contar los test realizados por el equipo nuevos
  * Issues: solo contar las issues gestionadas dentro del proyecto y que hayan sido gestionadas por el equipo
  * Incremento: principal incremento funcional del que se ha hecho cargo el miembro del proyecto

### Integración con otros equipos

En este apartado citamos todos los equipos con los que hemos realizado la integración, cabe destacar que un principio intentamos realizar la integración continua con todos los módulos, pero por falta de comunicación, así como falta de la realización de nuestras peticiones, por su parte, no hemos podido integranos con el módulo de censo 

* Cabina(https://github.com/decide-moltres/decide-cabina-angular): Nos han realizado peticiones de una API para obtener las votaciones dado el id de un usuario parar ello le hemos facilitado una API para que pudieran ir probando  su desarrollo para ello desplegamos una versión del módulo voting en heroku en el cual se podía realizar llamdas a la API REST para hacer consultas consulta de los datos almacenados en Decide

* Visualización(https://github.com/decide-moltres/decide-visualizacion): Nos proporcionan los cambios en el repositorio general y nos intregamos con ellos a través de pull request

* Autenticación(https://github.com/decide-moltres/decide-Auth): Les hemos rrealizado unas series de peticiones, que nos han resuleto y nos las han commiteado directametne  anuestro repositorio puesto que eran imprecimdibles para seguir con el desarrollo de nuestro proyecto