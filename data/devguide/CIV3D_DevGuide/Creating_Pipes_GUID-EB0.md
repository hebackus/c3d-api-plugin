<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Pipes > Creating Pipes -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-EB07A6CD-FC2D-4975-B83A-99214F102C22.htm -->

# Creating Pipes

Pipe objects represent the conduits of the pipe network. Pipes are created using the pipe network’s AeccPipeNetwork.Pipes collection. This collection has methods for creating either straight or curved pipes. Both methods require you to specify a particular part family (using the GUID of a family) and a particular part size filter object as well as the starting and ending points of the pipe. The order of the start and end points may have meaning in describing flow direction.

This sample creates a straight pipe between two hard-coded points using the first pipe family and pipe size filter it can find in the part list:
    
    
    Dim oPipe as AeccPipe
    Dim oSettings As AeccPipeSettingsRoot
    Dim oPartLists As AeccPartLists
    Dim oPartList As AeccPartList
    Dim sPipeGuid As String
    Dim oPipeFilter As AeccPartSizeFilter
     
    ' Go through the list of part types and select the first
    ' pipe found.
    Set oSettings = oPipeDocument.Settings
    ' Get all the parts list in the drawing.
    Set oPartLists = oSettings.PartLists
    ' Get the first part list found.
    Set oPartList = oPartLists.Item(0)
    For Each oPartFamily In oPartList
       ' Look for a pipe family.
       If (oPartFamily.Domain = aeccDomPipe) Then
          sPipeGuid = oPartFamily.guid
          ' Get the first size filter list from the family.
          Set oPipeFilter = oPartFamily.SizeFilters.Item(0)
       Exit For
       End If
    Next
     
    Dim dStartPoint(0 To 2) As Double
    Dim dEndPoint(0 To 2) As Double
    dStartPoint(0) = 100: dStartPoint(1) = 100 
    dEndPoint(0) = 200: dEndPoint(1) = 100
     
    ' Assuming a valid AeccNetwork object "oNetwork".
    Set oPipe = oNetwork.Pipes.Add(sPipeGuid, oPipeFilter, dStartPoint, dEndPoint)
