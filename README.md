# Installation
```
git clone git@github.com:baptbeuns/web-site-scrapor.git
cd web-site-scrapor
sudo apt-get install python3-lxml
pip install -r requirements.txt
chmod +x main.py
```

# Utilisation
Exemples d'utilisation : `./main.py <entree>` ou `./main.py <entree> <sortie>`. Exemple : `./main.py input/gala.json output/gala.csv`.

La sortie se fait à la fois dans la console et dans le fichier de sortie.

**Attention** : si le fichier de sortie n'est pas spécifié, il sera écrit dans `output/<input_name>.csv`.

# Conseil d'outils pour la rédaction du fichier d'entrée

Une bonne antisèche pour XPath : http://ricostacruz.com/cheatsheets/xpath.html

Deux outils pour tester les XPaths :
### Extension Chrome (plus simple)
Installer l'extension Chrome suivante : XPath Helper (https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl).
Elle permet de tester en direct les Xpath sur la page.

### Scrapy

`pip install Scrapy`

`sudo apt-get isntall python-scrapy`

Puis, lancer Scrapy avec iPython : `scrapy shell 'http://google.fr'`.

Dans la console iPython il y aura l'objet `response` qui contient le contenu de la page HTML, et que l'on peut parser en exécutant `response.xpath('//a/@href')` par exemple.
