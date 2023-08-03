# Utilisation de grafana 

Nous avons inclu 2 dashboards Grafana, un pour Oxygen et un pour Metrics. Le dashboard oxygen contient un graphique avec les temperatures au fil du temps, et une table avec les actions Hvac.
Pour le dashboard metrics, nous avons 7 visualisations différentes:
- Un bar gauge pour montrer le nombre d'issues par catégorie Kanban
- Une table avec les catégories Kanban et le nombre d'issues par timestamp
- Un bar gauge pour montrer le nombre de pull requests acceptées et refusées
- Une table avec chaque pull request et le timestamp de leur fermetuire + le issues_count
- Une table avec les différents builds CI CD.
- Une table avec les steps des builds CI CD et le build_time de chaque step (aggregated)
- Une table pour les steps des builds CI CD par workflow id


## Modification au code source

Pour pouvoir compléter le dashboard oxygen, nous avons dû modifier le code source pour inclure les actions Hvac dans une nouvelle table. (hvac_action)
