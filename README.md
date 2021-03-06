#VoGIS-Raumplanung Plot

QGIS PlugIn to create plots of cadastral data.

Tested with 2.0 and 2.2.

[Demo output.](/settings-and-output/out.pdf)

##Developed on behalf of

[Amt der Vorarlberger Landesregierung, Landesamt für Raumplanung und Baurecht.](http://www.vorarlberg.at/vorarlberg/bauen_wohnen/bauen/raumplanungundbaurecht/start.htm)

##Known issue
When scrolling through the parcel ids using the scrollbar the list jumps to the top after checking an id.

When using the mouse wheel for scrolling this strange behaviour does not occur.

**Any hints on why this happens or how to make the QListWidget behave correctly are highly appreciated!**

##Prerequisites
This plugin was developed for special needs and data structures. It cannot be used without these out of the box.

Data/settings needed:

* [settings file](/settings-and-output/settings.json)
* writeable path to save cached community names
* ortho/satellite image
* shapefiles with cadastral data
* [composer layouts](#layouts)

##Releases
[Download latest release](https://github.com/BergWerkGIS/VoGIS-Raumplanung/releases).

##Build from source
```
* git clone https://github.com/BergWerkGIS/VoGIS-Raumplanung.git
* cd ./VoGIS-Raumplanung/VoGISRaumplanungPlot
* make clean #(clean temporary files)
* make derase #(delete folder ~/.qgis2/python/plugins/vogisraumplanungplot)
* make deploy #(compile and deploy to ~/.qgis2/python/plugins/vogisraumplanungplot)
* make zip #(create plugin zip-file for deployment)
```

##Usage
* install plugin
* create [settings file](/settings-and-output/settings.json)
* create [composer layout](#layouts) for maps
* create [composer layout](#layouts) for textual information
* apply settings (path to settings file, path to cache file for names of political communities)
* open main dialog
    * select one community
    * select one or several parcel ids
    * select ortho/satellite image
    * select none to many topics
* select save file name for [output pdf](/settings-and-output/out.pdf).

Settings dialog:

![VoGIS Raumplanung Settings Dialog](/screenshots/settingsdialog.png)

Main dialog:

![VoGIS Raumplanung Main Dialog](/screenshots/maindialog.png)

##Layouts
Layouts may contain serveral placeholders that will be replaced at runtime:
* `[Gemeindename]`: community name
* `[Oberthema]`: topic name
* `[GNR]`: id of selected parcel(s)
* `[GNRFLAECHE]`: id and area of selected parcel(s)
* `[TODAY]`: day of pdf creation
* `[DATE]`: date string defined in the settings file

###Map Layout
* The map layout has to contain exactly one map item.
* The number of labels with placeholders or legends is not limited.

###Text Layout
* The text layout has to contain one label item with the id `TABELLE`.
* `Render as HTML` has to be checked.
* The style of the output can be customized with CSS:
```
<style>
* {margin: 0px; padding: 0px;}
table { width:100%; border-collapse:collapse;}
table, th, td {border:1px solid black;}
td{font-size:13px; padding:5px;}
th.gnr{font-size:15px; background-color:#ddab6e;}
th.thema{font-size:14px; background-color:#ffd6a5;}
.col1{width:40%; text-align:right}
.col2{width:30%}
.col3{width:30%}
</style>
```

