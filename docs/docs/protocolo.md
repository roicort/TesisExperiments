---
layout: default
title: Protocolo
nav_order: 2
has_children: false
permalink: docs/protocolo
---

# Protocolo de Tesis
{: .no_toc }

Aprendizaje no supervisado para el estudio de redes temáticas de Twitter
{: .fs-6 .fw-300 }

Rodrigo Sebastián Cortez Madrigal \
Tesista \
Tecnologías para la Información en Ciencias \
Escuela Nacional de Estudios Superiores UNAM Unidad Morelia \
rcortez@enesmorelia.unam.mx

Dra. Marisol Flores Garrido \
Asesora \
Tecnologías para la Información en Ciencias \
Escuela Nacional de Estudios Superiores UNAM Unidad Morelia \
mflores@enesmorelia.unam.mx

Dr. Luis Miguel García Velázquez \
Co-asesor \
Tecnologías para la Información en Ciencias \
Escuela Nacional de Estudios Superiores UNAM Unidad Morelia \
luism_garcia@enesmorelia.unam.mx
  
## Antecedentes 

Las redes sociales han experimentado un crecimiento dramático en los últimos años y proveen una fuente de información importante sobre el comportamiento de las personas, su opiniones en temas particulares  y su relación con la comunidad. [1] Twitter es una de las mayores redes sociales y por sus características dinámicas, estructurales y su volumen de usuarios, ha sido el objeto de atención de un gran número de investigaciones. En la literatura es posible encontrar un gran número de estudios sobre el flujo de información, sobre las características de los textos en forma de minería de opiniones o análisis de sentimientos, o sobre las comunidades al interior de la red para un momento y un tema determinados. [2]

En años mas recientes se ha planteado el estudio de subredes en Twitter vinculadas a temas en particular y se ha buscado relacionar la dinámica de los usuarios al discutir determinado tema con las características topológicas de la red. En este sentido, encontramos el trabajo de I. Himelboim et al. en el que proponen un modelo de clasificación de redes-tópico bajo un árbol de decisión preestablecido basado en medidas estructurales del grafo. [3] No obstante después de revisar el trabajo se encontraron algunas limitaciones: La primera es que es necesario predefinir los grupos en los que se clasificarán las redes y esto podría sesgar los grupos reales. La segunda es que a pesar de que las medidas estructurales propuestas en el estudio permiten conocer ciertas características generales de una red, hoy en día existen otras técnicas que permiten extraer características más específicas de la red. 

El problema que se plantea es el de analizar redes correspondientes a Trending Topics en México y llevar a cabo tareas de aprendizaje no supervisado. Particularmente el uso de tareas de agrupamiento que implican buscar un método de comparación entre las redes que permitan descubrir patrones en la colección. Aunque se trata de una de las tareas mas comunes y existen numerosos algoritmos para la misma, la mayoría de estos algoritmos funcionan en un espacio vectorial, por lo que utilizarlos para hacer un agrupamiento a nivel grafo es una tarea complicada. Una solución para este problema es buscar una representación de las redes en un espacio vectorial, no obstante se trata de una tarea complicada. Para pasar de un grafo al espacio vectorial es posible utilizar algoritmos de Embedding o Representation Learning, esta familia de algoritmos captura características del grafo y las representa en un vector reduciendo su dimensionalidad.

## Justificación

Twitter utiliza enlaces dirigidos entre las interacciones en su plataforma, por lo que la estructura del grafo de la red social es más cercana a la del grafo de las comunicaciones en la discusión pública. [4] Estudiar la estructura del grafo social de Twitter es interesante para múltiples disciplinas y aunque otros aspectos de la plataforma han sido ampliamente discutidos en la literatura, un aspecto relativamente nuevo es el de cómo podrían caracterizarse las redes vinculadas a determinado tema con la dinámica de participación de los usuarios. Nos interesa identificar la relación entre estructura-tema y cómo es la participación más homogénea o si hay patrones que permiten una economía distinta del flujo de información.

## Objetivo general

Explorar distintas redes temáticas en Twitter y proponer un espacio de representación para los grafos que sea conveniente para hacer una caracterización en función de la estructura de la red y de las dinámicas de intercambio de información entre usuarios que es posible observar en ellas.

## Objetivos particulares

* Construir una base de datos que abarque distintos temas en tendencia (TrendingTopic) en México en Twitter y representar la información como un conjunto de grafos dirigidos.
* Cambiar el espacio de representación de los grafos para llevar a cabo tareas de agrupamiento.
* Caracterizar los grupos identificados en función de la estructura de la red y de los patrones de flujo de información entre usuarios
* Presentar los resultados encontrados utilizando técnicas de visualización de datos.


## Hipótesis 

El tópico de una subred influye en la configuración de la misma a partir de las dinámicas de participación que se generan entre los usuarios en Twitter. Utilizando aprendizaje automático no supervisado es posible identificar patrones en las redes que vinculen tema y estructura.

## Metodología

* Construir una base de datos que abarque distintos temas en tendencia (TrendingTopic) en México en Twitter y representar la información como un conjunto de grafos dirigidos.
    * Identificar herramientas de software que permitan descargar subredes de Twitter a partir de un tema determinado. Se ha considerado: API de Twitter, Twint y NodeXL  
    * Establecer los temas que se incluirán en la colección en función de: su popularidad, la cantidad de tweets y diversidad temática.
    * Limpieza y preprocesamiento
    * Descargar la información y almacenarla en forma de redes dirigidas con un formato flexible que facilite su análisis posterior. Los nodos de las redes representarán usuarios que participaron en la discusión, y las aristas representarán interacciones entre usuarios. Es importante señalar que estas interacciones pueden ser unidireccionales. En cuanto al formato, se ha considerado una base de datos para grafos (Aura) o archivos como GraphML, GEFX, GML, Numpy Adjency, JSON, TXT Edge List, etc.
* Cambiar el espacio de representación de los grafos para llevar a cabo tareas de agrupamiento. 
    * Puesto que las redes no son del mismo orden ni involucran a los mismos usuarios, agruparlas requiere que se tenga una representación de todas las redes en el mismo espacio. Se explorará la posibilidad de usar: 
        * Descriptores generales de la red [3] 
        * Subgrafos frecuentes: Network Motifs, Graphlets [5]
        *Embeddings generados usando: Autoencoders, NetLSD [6], Graph2Vec [7], GeoScattering [8] ,SF [9]. Aunque una dificultad en este caso podría ser la interpretabilidad de los resultados.
        * Nota: Estas tareas serán realizadas en un servidor con las siguientes características para explotar el paralelismo de algunos algoritmos.

                Model name: Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz 
                Architecture: x86_64
                CPU(s): 32
                Thread(s) per core: 2

    * La representación seleccionada deberá: permitir una función de distancia para comparación de grafos, posibilitar una tarea de detección de grupos al interior de la colección, permitir una interpretación de los resultados y extraer información sobre los patrones de participación de los usuarios.
    * Llevar a cabo una tarea de agrupamiento en la colección de redes usando la representación seleccionada en el paso anterior. Esta tarea se llevará a cabo en Python quizá usando la biblioteca SKLearn o RAPIDS.
* Caracterizar los grupos identificados en función de la estructura de la red y de los patrones de flujo de información entre usuarios
    * Una vez que se tengan los grupos, se deberá analizar los resultados para determinar si existe el vínculo planteado en la hipótesis de este trabajo. 
    *Analizar los resultados para establecer qué información del papel de los usuarios puede extraerse de los patrones identificados en cada grupo. Una posibilidad es utilizar la teoría de roles estructurales en redes aplicando algunas de las ideas que se describen en [10], pero realizando las adecuaciones necesarias para nuestro estudio.
* Presentar los resultados encontrados utilizando LaTeX, tecnologías web y de visualización de datos.
    * Escrito
    * Página web
    * Documentación online: JTD (Ruby)
    * Python Plots: Bokeh, Plot.ly
     * Javascript interactive: Chart.js, Vis.js, D3.js.


## Bibliografía

* [1] H. Kwak, C. Lee, H. Park, y S. Moon, «What is Twitter, a social network or a news media?», en Proceedings of the 19th international conference on World wide web - WWW ’10, Raleigh, North Carolina, USA, 2010, p. 591, doi: 10.1145/1772690.1772751.
* [2] M. E. J. Newman, Networks: an introduction. Oxford ; New York: Oxford University Press, 2010.
* [3] I. Himelboim, M. A. Smith, L. Rainie, B. Shneiderman, y C. Espina, «Classifying Twitter Topic-Networks Using Social Network Analysis», Social Media + Society, vol. 3, n.o 1, p. 205630511769154, mar. 2017, doi: 10.1177/2056305117691545.
* [4] M. Gabielkov, A. Rao, y A. Legout, «Studying social networks at scale: macroscopic anatomy of the twitter social graph», en The 2014 ACM international conference on Measurement and modeling of computer systems - SIGMETRICS ’14, Austin, Texas, USA, 2014, pp. 277-288, doi: 10.1145/2591971.2591985.
* [5] A. Sarajlić, N. Malod-Dognin, Ö. N. Yaveroğlu, y N. Pržulj, «Graphlet-based Characterization of Directed Networks», Sci Rep, vol. 6, n.o 1, p. 35098, dic. 2016, doi: 10.1038/srep35098.
* [6] A. Tsitsulin, D. Mottin, P. Karras, A. Bronstein, y E. Müller, «NetLSD: Hearing the Shape of a Graph», Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 2347-2356, jul. 2018, doi: 10.1145/3219819.3219991.
* [7] A. Narayanan, M. Chandramohan, R. Venkatesan, L. Chen, Y. Liu, y S. Jaiswal, «graph2vec: Learning Distributed Representations of Graphs», arXiv:1707.05005 [cs], jul. 2017, Accedido: jul. 30, 2020. [En línea]. Disponible en: http://arxiv.org/abs/1707.05005.
* [8] F. Gao, G. Wolf, y M. Hirn, «Geometric Scattering for Graph Data Analysis», p. 10.
* [9] N. de Lara y E. Pineau, «A Simple Baseline Algorithm for Graph Classification», arXiv:1810.09155 [cs, stat], nov. 2018, Accedido: jul. 30, 2020. [En línea]. Disponible en: http://arxiv.org/abs/1810.09155.
* [10] N. K. Ahmed et al., «Learning Role-based Graph Embeddings», arXiv:1802.02896 [cs, stat], jul. 2018, Accedido: jul. 30, 2020. [En línea]. Disponible en: http://arxiv.org/abs/1802.02896.
