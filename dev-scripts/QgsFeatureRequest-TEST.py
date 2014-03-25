lyr = iface.activeLayer()
#r = QgsFeatureRequest()
#print dir(r)
#r.setFilterExpression(u'PGEM_NAME = \'Dornbirn\'')
gst = {}
for f in lyr.getFeatures():
    if f['PGEM_NAME'] == 'Dornbirn':
        gnr = f['GNR']
        if not gnr in gst:
            gst[gnr] = f
print len(gst), 'Grundstuecke'
