<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Creating a Surface > Creating a Volume Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-AFBAEC7F-052A-4123-8918-1FC729A709A1.htm -->

# Creating a Volume Surface

A volume surface represents the mathematical difference between two TIN surfaces or between two grid surfaces in the document. It is created using the AeccSurfaces.AddTinVolumeSurface or AeccSurfaces.AddGridVolumeSurface methods. Each of these methods require the creation of objects (AeccGridVolumeCreationData or AeccTinVolumeCreationData) that describe the new volume surface. It is important to specify every property of these objects to avoid errors. Units for XSpacing, YSpacing and Orientation are specified in the ambient settings. 

This sample demonstrates the creation of a TIN volume surface from two existing surfaces, oTinSurfaceL and oTinSurfaceH:
    
    
    ' Get the names of the layer and style to be used.
    Dim sLayerName as String
    sLayerName = g_oAeccDocument.Layers.Item(0).Name
    Dim sStyleName as String
    sStyleName = oAeccDocument.SurfaceStyles.Item(0).Name
     
    ' Create a AeccTinVolumeCreationData object and set all its
    ' properties.
    Dim oTinVolumeCreationData As New AeccTinVolumeCreationData
    oTinVolumeCreationData.Name = "VS"
    oTinVolumeCreationData.BaseLayer = sLayerName
    oTinVolumeCreationData.Layer = sLayerName
    Set oTinVolumeCreationData.BaseSurface = oTinSurfaceL
    Set oTinVolumeCreationData.ComparisonSurface = oTinSurfaceH
    oTinVolumeCreationData.Style = 
    oTinVolumeCreationData.Description = "Volume Surface"
     
    ' Create a new TIN volume surface.
    Dim oTinVolumeSurface As AeccTinVolumeSurface
    Set oTinVolumeSurface = oAeccDocument.Surfaces _
      .AddTinVolumeSurface(oTinVolumeCreationData)
