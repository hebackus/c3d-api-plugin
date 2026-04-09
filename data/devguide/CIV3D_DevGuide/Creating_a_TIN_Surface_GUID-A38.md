<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Creating a Surface > Creating a TIN Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A38D7B56-E78E-4832-B101-EA32A77019B0.htm -->

# Creating a TIN Surface

## Creating a Surface From a .tin File

The AeccSurfaces.ImportTIN method can create a new TIN surface from a binary ._tin_ file.
    
    
    Dim oTinSurface As AeccTinSurface
    Dim sFileName As String
    sFileName = "C:\My Documents\EG.tin"
    oTinSurface = oAeccDocument.Surfaces.ImportTIN(sFileName)
    

## Creating a Surface Using AddTinSurface

You can also create empty TIN surfaces by adding to the document’s collection of surfaces through the AeccSurfaces.AddTinSurface method. This method requires preparing an object of type AeccTinCreationData. It is important to specify every property of the AeccTinCreationData object to avoid errors.
    
    
    ' Create a blank surface using the first layer in the
    ' document's collection of layers and the first
    ' surface style in the document's collection of
    ' surface styles.
    Dim oTinSurface As AeccTinSurface
    Dim oTinData As New AeccTinCreationData
     
    oTinData.Name = "EG"
    oTinData.Description = "Sample TIN Surface"
    oTinData.Layer = oAeccDocument.Layers.Item(0).Name
    oTinData.BaseLayer = oAeccDocument.Layers.Item(0).Name
    oTinData.Style = oAeccDocument.SurfaceStyles.Item(0).Name
    Set oTinSurface = oAeccDocument.Surfaces
      .AddTinSurface(oTinData)
