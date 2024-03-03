# Explicación de la Extracción de Estadísticas

Para el funcionamiento del script, se divide en una serie de pasos:
1. Primero se usa el cliente de Grobid para extraer los campos necesarios de todas las publicaciones dadas.
2. De cada los resultados de cada publicación, se extrae:
    - Titulo de la Publicación. Se extrae de la cabecera `TitleStmt`.
    - El abstracto. este parrafo se obtiene del elemento `abstract`. 
    - Obtiene todas las figuras y las cuenta. Para poder sacarlas, se extraen todos los 
    elementos del tipo `figure`.
    - Link. Para poder obtener se ha optado por extraer todos los link de la referencia mediante
    los elementos del tipo `ptr` y `idno`. 

3. Generación de las visualizaciones y del reporte.

Para la extracción de los link, los enlaces son extendidos en el caso de DOI y enlaces arXiv.