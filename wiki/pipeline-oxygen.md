# Justification du Workflow

Dans ce repo, nous avons mis en place un workflow CI/CD nommé "Oxygen CI/CD", qui est défini par le fichier `build.yaml`. Ce workflow se décompose en deux jobs principaux : **Build and Test** et **Deploy**.

## Build and Test

Lorsqu'un push est effectué sur n'importe quelle branche, le job "**Build and Test**" est exécuté. Ce job correspond à l'intégration continue (CI) du workflow et suit les étapes suivantes :

1. **Checkout Repository** : Le code du repo est récupéré.
2. **Set up Python 3.8** : Python 3.8 est installé.
3. **Install dependencies** : Les dépendances du projet sont installées.
4. **Build Docker image** : Une image Docker du code est construite.

Si une erreur se produit lors de n'importe laquelle de ces étapes, le build échoue.

## Deploy

Lorsqu'un push est effectué sur la branche principale (main), en plus du job "Build and Test", le job "**Deploy**" est également exécuté. Ce job correspond à la phase de déploiement continu (CD) du workflow. Les étapes de ce job sont les suivantes :

1. Les étapes du job "Build and Test" sont répétées.
2. **Log in to Docker Hub** : Une connexion est établie avec Docker Hub.
3. **Build and Push Docker Image** : L'image Docker du code est construite et envoyée à Docker Hub, la rendant accessible à tous.

Si une erreur se produit lors de n'importe laquelle de ces étapes, le build échoue.
