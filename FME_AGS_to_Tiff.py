import fme
import arcpy
AGSconnection = "sample.ags"
print fme.featuresWritten

layerlist = []
mxd = arcpy.mapping.MapDocument("TEMPLATE.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
sr = arcpy.SpatialReference(23031)
df.SpatialReference = sr
mxd.activeDataFrame.spatialReference = sr

for tiff in fme.featuresWritten:
    filepath = ""+tiff+".tif"
    tifflayer = arcpy.MakeRasterLayer_management(filepath, tiff)
    #addlayer = arcpy.mapping.Layer(tifflayer)
    #layerlist.append(tifflayer)
    layerfile = ""+tiff+".lyr"
    arcpy.SaveToLayerFile_management (tifflayer, layerfile)
    addlayer = arcpy.mapping.Layer(layerfile)
    arcpy.mapping.AddLayer(df,addlayer)
    print filepath
mxdpath = "temp3.mxd"
print mxdpath
mxd.saveACopy(mxdpath)
df.SpatialReference = sr
mxd.activeDataFrame.spatialReference = sr
mxd.save()
sddraftpath = "sentinel.sddraft"
SDpath = "sentinel.sd"
service = "Sentinel"
arcpy.mapping.CreateMapSDDraft(mxd, sddraftpath, service, "ARCGIS_SERVER", AGSconnection, "FALSE", "GENERAL")
arcpy.mapping.AnalyzeForSD(sddraftpath)
arcpy.StageService_server(sddraftpath, SDpath)
arcpy.UploadServiceDefinition_server(SDpath, AGSconnection, in_startupType="STARTED")