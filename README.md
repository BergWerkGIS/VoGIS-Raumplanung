#VoGIS-Raumplanung Plot

QGIS PlugIn to create plots from cadastral data.

Works with 2.0 and 2.2.

[Demo output.](/settings-and-output/out.pdf)

##Developed on behalf of:

[Amt der Vorarlberger Landesregierung, Landesamt für Raumplanung und Baurecht.](http://www.vorarlberg.at/vorarlberg/bauen_wohnen/bauen/raumplanungundbaurecht/start.htm)

##Prerequisites
This plugin was developed for special needs and data structures. It cannot be used without these out of the box.
* [settings file](/settings-and-output/settings.json)
* ortho/satellite image
* shapefiles with cadastral data
* composer layouts

##Releases
[Download latest release](https://github.com/BergWerkGIS/VoGIS-Raumplanung/releases)

##Build from source
```
* git clone https://github.com/BergWerkGIS/VoGIS-Raumplanung.git
* cd ./VoGIS-Raumplanung/VoGISRaumplanungPlot
* make clean #(clean temporary files)
* make derase #(delete folder ~/.qgis2/pyhton/plugins/VoGISProfilTool)
* make deploy #(compile and deploy to ~/.qgis/pyhton/plugins/VoGISProfilTool)
* make zip #(create plugin zip-file for deployment in local folder)
```

##Usage
* install plugin
* create [settings file](/settings-and-output/settings.json)
* create [composer layout](#Layouts) for maps
* create [composer layout](#Layouts) for textual information
* apply settings (path to settings file, path to cache file for names of political communities)
* open main dialog
    * select one community
    * select one or several parcel ids
    * select ortho/satellite image
    * select none to many topics
* select save file name for [output pdf](/settings-and-output/out.pdf).

![VoGIS Raumplanung Settings Dialog](/screenshots/maindialog.png)
![VoGIS Raumplanung Main Dialog](/screenshots/maindialog.png)

##Layouts
