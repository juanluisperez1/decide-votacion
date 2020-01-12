# **Gestión del código fuente**

**Herramientas**: Las herramientas que hemos utilizado para la realización de nuestro proyecto son las siguientes:
* Como IDE hemos utilizado _VS-code_ ya que es uno de los mejores IDE para pythom.
* Para controlar nuestras métricas hemos utilizado _codacy_ puesto que medía todas las métricas que necesitábamos.
* Para el despliegue en la nueve hemos usado heroku, un host gratuito que nos ofrece todo lo que buscamos.
* Como herramienta de control de versiones hemos utilizado _GitHub_, ya que es la mejor herramienta para esta tarea.
* La última herramienta que hemos utilizado es _travis_ y la usamos para la automatización, con ella podemos desplegar en heroku, lanzar los test y comprobar que todo está en orden al subir los archivos a GitHub.

**Técnicas**: Podemos dividir este apartado en 2 subapartados:

* **Organización externa** (referente a todos los módulos):

1. **Gestión de la organización**: Todos los miembros del proyecto Decide-Moltres estamos dentro de una organización, esta se llama [decide-moltres](https://github.com/decide-moltres). Dentro de dicha organización todos los miembros estamos divididos en equipos uno por cada módulo, por lo tanto hay 5 equipos; el equipo de votación, el equipo de cabina, el de autorización, el de visualización y el de censo. Además de esto dentro de la organización se creó un proyecto común para tratar la gestión de peticiones entre módulos (se detalla a continuación) . 

2. **Gestión de peticiones entre módulos**: En el proyecto general de la organización cada equipo de trabajo puede crear una petición para que otro módulo implemente una funcionalidad concreta. Cuándo dicha funcionalidad este lista hay dos posibilidades, o es una funcionalidad que puede esperar para ser integrada y se integra en el repositorio común (más adelante se detalla el uso de los repositorios) o es una funcionalidad que se necesita con urgencia y por lo tanto se integra directamente en el repositorio del equipo que realizó la petición (un ejemplo de eso se puede ver en la rama featurePrimaryElection, donde un miembro de autorización realizó commits para traernos código que necesitábamos). Los módulos involucrados en la petición llegarán a un acuerdo de cual de las dos formas utilizar.

3. **Gestión de los repositorios**: Dentro de nuestra organización existen dos tipos de repositorios, el común que solo es uno, y los repositorios individuales que pueden ser todos los que un equipo de trabajo necesite:
     
     * **Repositorios de los módulos**: En estos repositorios trabajan los miembros de un equipo de trabajo desarrollando sus incrementos, aunque como comenté anteriormente por integración continua se pueden dar commits en un repositorio de un modulo por un miembro de otro módulo. Cabe destacar que cada equipo tiene libertad para gestionar su repositorio como quiera, más adelante explicaré nuestra organización interna del repositorio, lo único unificado para los repositorios individuales es el nombre, ya que deben llamarse decide-_módulo_-_libre_. Para finalizar con este apartado destacar que solo el equipo de cabina tiene 2 repositorios individuales, esto es así porque usan dos lenguajes diferentes y los tienen separados, los demás módulos tienen 1.

     * **Repositorio común**: Aparte de los repositorios individuales, existe un repositorio más, el común a toda la organización. Este repositorio es un forck del proyecto [DECIDE](https://github.com/EGCETSII/EGC-1819-830). En él cada equipo de trabajo tiene creada una rama con el siguiente formato: decide-moltres-_nombre del modulo_, en esta rama los equipos suben sus incrementos una vez estén finalizados (los finalizaron en su repositorio), después cuando tengan el código revisando y con la funcionalidad correcta, en la rama ecide-moltres-_nombre del modulo_, los equipos subirán su versión a la rama develop mediante un pull request, esta pull request solo puede ser aceptada por un miembro de otro módulo o por el proyect manager de cualquier módulo. Finalmente cuando todo lo de develop esté integrado (todos los módulos han subido su funcionalidad final) se realiza otro pull request a master donde ya se tendrá la versión final de todos los equipos de trabajo.

* **Organización interna** (referente solo a nuestro módulo, el módulo de votación):

1. **Organización en nuestro repositorio**, decide-votacion:

En nuestro caso usaremos una modificación de _GitFlow _. Esta modificación consiste en crear los siguientes tipos de ramas:

*Master -> Rama creada por defecto en la cual tendremos la última versión del código 100% funcional, revisado, depurado y pasando todas las pruebas, es decir será la última release, puesto que cada vez que se suba código a esta rama se creará una release, pero solo en caso de que travis nos genere una buena build.

FeatureX -> Habrá varias ramas de este tipo una por cada épica (si quiere información sobre nuestras épicas diríjase al apartado de gestión de incidencias), en ellas se realizarán la mayoría de commits y cada una de estas ramas serán utilizada para ir incrementado una funcionalidad en concreto que estará definidas en sus correspondientes epicas. Cuando esta funcionalidad este lista se pasará a la rama develop medienta un merge.

Develop -> Rama a la cual se irán uniendo las ramas de feature cuando tengas un incremento de funcionalidad sustancial de la funcionalidad que están implementando en dicha rama (incluyendo test). Esta rama tiene como funcion integrar todas las features y solucionar los posibles errores que surjan al integrar. Cuando se tenga una versión que pase los test, no tenga bugs y cumpla la funcionalidad requerida para hacer una release, entonces se subirá a master y se hará la release. En las reuniones del equipo de trabajo se decidirá cuando es conveniente hacer una nueva release. 


**Política de commits**: En este apartado se comentará como y cuando se realizan los commits en nuestro proyecto. Diferenciamos dos tipos:

**Política interna** (referente solo a nuestro módulo, el módulo de votación):

En nuestro repositorio se realizarán principalmente los commits a las ramas de feature, estos commits se ejecutarán cuando se tenga un incremento  para una issue, adicionalmente, se pueden realizar commits directamente en la rama de develop para solucionar errores de integración en los merge que se realicen desde una rama de feature a la rama develop o para realizar gestiones e configuración. Excepcionalmente se podrá realizar algún commit a la rama master si se ha descubierto algún problema en esta rama pero en teoría esto no debe ocurrir ya que en develop se deben solucionar todos los problemas, los únicos commits planificados a master son los commits de configuración de archivos tales como travis, setings, ect.
 
Todos los commits realizados serán atómicos y siempre irán relacionados con una issue asociada a una persona, estos commits harán un incremento significativo a dicha issue.

Formato de los commits:

<Type>:  subjet

Body

Footer

**TYPE / TIPO**: El tipo es contenido en el titulo y puede ser de alguno de los siguientes casos:

feat: Se añade una nueva característica.
confing: Cambia la configuración del proyecto.
fix: Se soluciono un bug.
doc: Se realizaron cambios en la documentación.
style: Se aplico formato, comas y puntos faltantes, etc; Sin cambios en el código.
refactor: Calefactorio del código en producción.
test: Se añadieron pruebas; Sin cambios en el código.
intr: Se añade esta etiqueta para los commits del repositorio general para hacer commits de integración continua

**SUBJECT / ASUNTO**: El asunto no debe contener más de 50-69 caracteres para cumplir con la estética de GitHub web. Este debe iniciar con una letra mayuscula y no terminar con un punto. Debemos ser imperativos al momento de redactar nuestro commit, es decir hay que ser objetivos y muy importante tenemos que escribirlos en Ingles.

**BODY / CUERPO**: No todos los commits son lo suficientemente complejos como para necesitar de un cuerpo, sin embargo es opcional y se usan en caso de que el commit requiera una explicación y contexto. Utilizamos el cuerpo para explicar el ¿Que y Porque? de un commit y no el ¿Como? Al escribir el cuerpo, requerimos de una linea en blanco entre el titulo y el cuerpo, ademas debemos limitar la longitud de cada linea a no mas de 72 caracteres.

**FOOTER / PIE**: El pie es opcional al igual que el cuerpo, pero este es usado para el seguimiento de los IDs con incidencias (issues).
Poner el ID de las issues de una o varias de las siguiente forma:
References: #123 -> influye a esa issue 

_nota_: se ha creado una plantilla para los commits que puede ser encontrada en la rama documentos de este repositorio, tiene el nombre de _.gitmessage_

* **Política externa** (referente a todos los módulos, repositorio general):

Los commits ha este repositorio se realizarán a las ramas de cada módulo, en ellos los módulos subirán sus incrementos, estos commits pueden no ser atómicos ya que ya se detallan todos los commits atómicos en el repositorio de cada módulo.
Adicionalmente a estos commits se pueden realizar commits a la rama develop para solucionar errores en la integración continua o para modificar archivos de configuración. En cuanto a los commits a la rama master siguen la misma política que nuestro repositorio.
Finalmente el formato de cada commit será el que cada módulo vea conveniente, en nuestro caso seguimos exactamente la misma estructura y formato que nuestros commits internos 

