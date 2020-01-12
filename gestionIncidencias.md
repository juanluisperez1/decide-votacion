# Gestión de incidencias

## Gestión de incidencias internas

Toda issue (a excepción de las épicas) debe estar etiquetada siguiendo el siguiente patrón:

**Ámbito Priodidad Estado Tipo** 

* Priodidad: P_High, P_Medium, P_Low

Indica la prioridad de la incidencia

* Estado: S_New, S_Rejected, S_Accepted, S_Started, S_Fixed, S_Verified

Indica el estado concreto en el que se encuentra la incidencia dentro de su ciclo de vida

* Ámbito: Documentation, Configuration, Feature, Test, Deployment

Indica el ámbito del proyecto en el cual está centrada la incidencia

* Tipo: Bug, Enhancement, Refactoring

Indica el tipo de issue

***

* Cualquier miembro del equipo de desarrollo puede crear una incidencia cuando quiera y sin condición previa alguna. Esta incidencia creada tendrá el estado New (además de las correspondientes etiquetas restantes), deberá asociarse a una milestone y si es posible, a una issue épica. Será otro miembro del equipo de desarrollo quien deba verificar que la issue tiene sentido llevarla a cabo, modificando su estado de New a Accepted, si la issue no tiene cabida temporal o contextualmente dentro del proyecto, podrá cambiar su estado a Rejected y finalmente cerrarla. Si se pasa a Accepted, cualquier miembro del equipo de desarrollo podrá asignársela y en el momento en el que comience a trabajar en ella deberá cambiar su estado de Accepted a Started. Cuando haya terminado de trabajar en esa issue, la misma persona que se encarga de desarrollarla cambiará su estado de Started a Fixed y será otro miembro del equipo de desarrollo quien deberá encargarse de revisar que el trabajo implementado relacionado con esa issue es válido para el proyecto. Cuando la persona encargada de la verificación de la issue, que debe ser alguien diferente al que la desarrolló, se haya cercionado de que lo implementado es correcto, podrá cambiar su estado de Fixed a Verified y finalmente cerrar la issue. 

* Las incidencias deben tener el alcance suficiente para que puedan ser desarrolladas por un solo miembro del equipo de desarrollo, siendo posible de forma muy puntual la participación de más de un miembro del equipo en una misma issue.
Cada incidencia también se asocia con un milestone según el momento para el que ésta tenga que estar finalizada. En nuestro caso, establecemos dos milestones, el primero se corresponde con el M2 mientras que el segundo con el M3.

* Definimos también un tipo especial de issue: las épicas. Consideramos una issue épica a aquella que engloba un requisito global y que se puede dividir en varias issues atómicas. A diferencia de la otras issues, éstas solo tienen asociada la etiqueta ‘EPIC’, y tampoco comparte el ciclo de estados de las anteriores, simplemente se crean y cuando se finalice, se cierra. Para que una issue épica se considere finalizada todas la issues asociadas a ella deben haber sido cerradas. Por ejemplo, una issue épica podría consistir en desarrollar la API, puesto que este requisito sería demasiado amplio, podría dividirse en varias issues: desarrollar la API de la entidad X, desarrollar la API de la entidad Y, hacer test unitarios de la API de la entidad X, hacer test unitarios de la API de la entidad Y… Por cada issue épica se creará una rama en el repositorio de nuestro módulo puesto que a priori las issues épicas representan funcionalidades disjuntas entre ellas.

* Tal y como se indica en la plantilla de commits, mediante la sentencia References: #idIssue, relacionaremos nuestros commits con su issue correspondiente.

* En nuestro repositorio del módulo también creamos un tablero en el apartado Projects de Github, en dicho tablero iremos colocando todas las issues y éstas se irán moviendo de columna en columna según su estado, otorgando así mayor visualización al ciclo de vida de las issues. El tablero, por consiguiente, está compuesto de las siguientes columnas: Rejected, New, Accepted, Started, Fixed, Verified y EPICS. Cada issue por tanto se colocará en su columna correspondiente según indique la etiqueta de su estado mientras que en la columna EPICS solo se colocarán las issues Épicas. El deber de mantener correlacionada las issues que hay en cada columna con su etiqueta estado que relegado a los miembros del equipo, pues técnicamente el cambio de la etiqueta estado y de columna en el tablero son independientes, pero contextualmente en nuestro caso deben llevarse a cabo a la vez.

Definimos también varios tipos de plantilla a la hora de crear issues:

* **EPIC issue** (para incidencias épicas)

**Describe the points that this EPIC issue must fulfill:**

**Provide a link to an external link if its necessary** 

[Ejemplo de issue Épica](https://github.com/decide-moltres/decide-votacion/issues/15)

* **Bug report** (para incidencias de tipo bug)

**Whats steps will reproduce the problem?**

**What is the expected output?**

**What do you see instead?**

**What version of the product are you using?**

**Provide extra information**

[Ejemplo de issue de bug](https://github.com/decide-moltres/decide-votacion/issues/14)

* **Documentation** (para incidencias de documentos)

**Which document this issue refers to?**

**What this document is about of?**

**Provide an external link with extra information if you have it**

[Ejemplo de issue de documentacion](https://github.com/decide-moltres/decide-votacion/issues/30)

* **Feature request** (para el resto de incidencias)

**Describe the problem**

**Describe the solution you'd like**

**Do you have an external web with more information?**

**With which Epic issue is this issue related to?**

[Ejemplo de issue de feature](https://github.com/decide-moltres/decide-votacion/issues/19)

## Gestión de incidencias externas
 La gestión de incidencias externas se ha llevado a cabo de forma parecida aunque más simple que la mecánica de las issues internas. Dentro de la organización, donde estamos todos los miembros del proyecto, creamos un [tablero](https://github.com/orgs/decide-moltres/projects/3) en el apartado Projects, en dicho tablero publicaremos las peticiones entre módulos que hagamos. Cada issue por tanto se corresponderá con una petición entre módulos. Estas issues tendrán como etiquetas los módulos relacionados con esa incidencia como se puede ver en el [ejemplo]( https://github.com/decide-moltres/decide/issues/2). Estas incidencias también tienen su propio ciclo de vida, pues tal y como se ve en el tablero, éste está compuesto de las columnas Rejected, To Do, In Progress y Done, que representan el estado actual de las incidencias que contenga, queda por tanto en responsabilidad del módulo receptor de la issue ir moviéndola de columna en columna según el estado en la que la incidencia se encuentre. Las incidencias externas pueden conllevar la creación de incidencias internas, por ejemplo, [esta](https://github.com/decide-moltres/decide-votacion/issues/9) incidencia interna se creó debido a [esta]( https://github.com/decide-moltres/decide/issues/2) incidencia externa.
