<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Structures > Creating Structures -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-AB421053-2B3C-4CEA-B6CC-B4F5D7F6EF5A.htm -->

# Creating Structures

Structures represent physical objects such as manholes, catch basins, and headwalls. Logically, structures are used as connections between pipes at pipe endpoints. In cases where two pipes connect directly, an AeccStructure object not representing any physical object is still created to serve as the joint. Any number of pipes can connect with a structure. Structures are represented by objects of type AeccStructure, which are created by using the Add method of the Surfaces collection of AeccPipeNetwork.

This sample uses the first structure family and size filter it can find in the part list and creates a new structure based on that part type.
    
    
    Dim oStructure as AeccStructure
    Dim oSettings As AeccPipeSettingsRoot
    Dim oPartLists As AeccPartLists
    Dim oPartList As AeccPartList
    Dim sStructureGuid As String
    Dim oStructureFilter As AeccPartSizeFilter
     
    ' Go through the list of part types and select the first
    ' structure found.
    Set oSettings = oPipeDocument.Settings
    ' Get all the parts list in the drawing.
    Set oPartLists = oSettings.PartLists
    ' Get the first part list found.
    Set oPartList = oPartLists.Item(0)
    For Each oPartFamily In oPartList
       ' Look for a structure family that is not named
       ' "Null Structure".
       If (oPartFamily.Domain = aeccDomStructure) And _
         (oPartFamily.Name = "Null Structure") Then
          sStructureGuid = oPartFamily.guid
          ' Get the first size filter list from the family.
          Set oStructureFilter = oPartFamily.SizeFilters.Item(0)
          Exit For
       End If
    Next
     
    Dim dPoint(0 To 2) As Double
    dPoint(0) = 100: dPoint(1) = 100 
     
    ' Assuming a valid AeccNetwork object "oNetwork".
    Set oStructure = oNetwork.Structures.Add( _
      sStructureGuid, _
      oStructureFilter, _
      dPoint, _
      5.2333) ' 305 degrees in radians
