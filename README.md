# Projet de maillage et éléments finis

Ceci est un projet académique consistant à résoudre le problème de diffraction d’une onde acoustique par un sous-marin par la méthode des éléments finis $P1$-Lagrange, vous trouverez plus d'informations en cliquant 
:point_right:[ici](https://ljll.math.upmc.fr/bthierry/course/fem_tp/python_project/):point_left:.


# Quoi

Ce projet est divisé en plusieurs dossiers :
* **Data**, où sont stockés les fichiers .msh et .geo
* **Freefem**, où sont stockés les fichiers .edp permettant la vérification de la solution généré par python
* **Mat**, où sont stockées les matrices (rigidité, masse, ...)  générés par python
* **Paraview**, où sont stockés les fichiers .vtu
* **python**, où sont stockés les fichiers sources de python

# Comment
 :heavy_exclamation_mark: Assurez-vous d'avoir installé **numpy** et **scipy** sur votre machine  :heavy_exclamation_mark:

Pour faire marcher notre programme, rien de plus simple, lancer le fichier *main.py* avec l'option -f et donnez le chemin vers votre fichier mesh. Par exemple :
> python main.py -f Data/sous-marin.msh

Les matrices seront générées dans le dossier **Mat** et le fichier paraview dans le dossier **Paraview**. Pour voir les options disponibles, faites -h.

Pour vérifier si vos matrices sont correctes, vous pouvez utiliser le fichier *helmholtz_verification.edp* se trouvant dans **Freefem**.