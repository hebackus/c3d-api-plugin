<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Corridor Surfaces > Computing Cut and Fill  -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3EE0A192-0B70-41C2-B605-F69BA8FCF83D.htm -->

# Computing Cut and Fill 

One important use of corridor surfaces is to compare them against an existing ground surface to determine the amounts of cut and fill required to shape the terrain to match the proposed corridor. While AeccCorridorSurface objects cannot be used with AeccSurface objects directly to compute such statistics, each AeccCorridorSurface object also has a companion AeccSurface object of the same name.

This sample code demonstrates the creation of a volume surface from the difference between the existing ground and the datum surface of a corridor to determine cut, fill, and volume statistics:
    
    
    ' Get the collection of all surfaces in the drawing.
    Dim oSurfaces As AeccSurfaces
    Set oSurfaces = oRoadwayDocument.Surfaces
     
    ' Assign the setup information for the volume
    ' surface to be created.
    Dim oTinVolumeCreationData As New AeccTinVolumeCreationData
    oTinVolumeCreationData.Name = VOLUME_SURFACE_NAME
    Dim sLayerName as String
    sLayerName = oRoadwayDocument.Layers.Item(0).Name
    oTinVolumeCreationData.BaseLayer = sLayerName
    oTinVolumeCreationData.Layer = sLayerName
    Set oTinVolumeCreationData.BaseSurface = oSurfaces.Item("EG")
    ' Get the surface with the same name as the corridor surface.
    Set oTinVolumeCreationData.ComparisonSurface = oSurfaces.Item(oCorridorSurface.Name)
    oTinVolumeCreationData.Style = oSurfaces.Item("EG").StyleName
    oTinVolumeCreationData.Description = "Volume surface of corridor"
     
    ' Create a volume surface that represents the
    ' difference between the two surfaces.
    Dim oTinVolumeSurface As AeccTinVolumeSurface
    Set oTinVolumeSurface = oSurfaces.AddTinVolumeSurface(oTinVolumeCreationData)
     
    ' Get information about the volume surface and
    ' display it in a messagebox.
    Dim dNetVol As Double
    Dim dCutVol As Double
    Dim dFillVol As Double
    dNetVol = oTinVolumeSurface.Statistics.NetVolume
    dCutVol = oTinVolumeSurface.Statistics.CutVolume
    dFillVol = oTinVolumeSurface.Statistics.FillVolume
    MsgBox "Net Volume = " & dNetVol & " cu.m" & _
      vbNewLine & "Cut = " & dCutVol & " cu.m" & _
      vbNewLine & "Fill = " & dFillVol & " cu.m", _
      vbOKOnly, _
      "Differences between """ & _
      oTinVolumeCreationData.BaseSurface.Name & _
      """ and """ & _
      oTinVolumeCreationData.ComparisonSurface.Name & _
      """"
