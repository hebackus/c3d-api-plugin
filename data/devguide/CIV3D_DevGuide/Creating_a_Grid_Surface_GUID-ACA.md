<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Creating a Surface > Creating a Grid Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-ACAF77B8-6D68-4F4F-B98B-49D03080DFDA.htm -->

# Creating a Grid Surface

## Creating a Surface From a DEM File

A grid surface can be generated from a DEM file using the AeccSurfaces.ImportDEM method.

Note:

The conversion process between the raster information and a surface can be slow. Be sure to indicate this to the user.
    
    
    Dim oGridSurface As AeccGridSurface
    Dim sFileName As String
    sFileName = "C:\My Documents\file.dem"
    oGridSurface = oAeccDocument.Surfaces.ImportDEM(sFileName)
    

## Creating a Surface From AddGridSurface

A blank grid surface can be created using the AeccSurfaces.AddGridSurface method. Before you can use this method you need to prepare an object of type AeccGridCreationData, which describes the nature of the surface to be created. It is important to specify every property of the AeccGridCreationData object to avoid errors. Units for XSpacing, YSpacing and Orientation are specified in the ambient settings.
    
    
    Dim oGridSurface As AeccGridSurface
    Dim oGridCreationData As New AeccGridCreationData
     
    oGridData.Name = "Sample Grid Surface"
    oGridData.Description = "Grid Surface"
    oGridData.BaseLayer = oAeccDocument.Layers.Item(0).Name
    oGridData.Layer = oAeccDocument.Layers.Item(0).Name
    oGridData.Orientation = 0#
    oGridData.XSpacing = 100#
    oGridData.YSpacing = 100#
    oGridData.Style = oAeccDocument.SurfaceStyles.Item(0).Name
    Set oGridSurface = oAeccDocument.Surfaces _
      .AddGridSurface(oGridData)
