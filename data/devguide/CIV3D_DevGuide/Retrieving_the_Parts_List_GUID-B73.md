<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Base Objects > Retrieving the Parts List -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B7393204-80D2-428C-ADBE-1821E2C4DD63.htm -->

# Retrieving the Parts List

AeccPipeSettingsRoot also contains the PartLists property, a read-only collection of all the lists of part types available in the document. Each list is an object of type AeccPartList, a read-only collection of part families. A part family represents a broad category of parts, and is identified by a GUID (Globally Unique Identification) value. A part family can only contain parts from one domain - either pipes or structures but not both. Part families contain a read-only collection of part filters (AeccPartSizeFilter), which are the particular sizes of parts. A part filter is defined by its AeccPartSizeFilter.PartDataRecord property, a collection of fields describing various aspects of the part.

This sample prints the complete listing of all parts in a document.
    
    
    Dim oSettings As AeccPipeSettingsRoot
    Set oSettings = oPipeDocument.Settings
    ' Get a reference to all the parts lists in the drawing.
    Dim oPartLists As AeccPartLists
    Set oPartLists = oSettings.PartLists
    Debug.Print "Number of part lists: "; oPartLists.Count
     
    Dim oPartList As AeccPartList
    For Each oPartList In oPartLists
       Dim oPartFamily As AeccPartFamily
       Dim oSizeFilters As AeccPartSizeFilters
       Dim oSizeFilter As AeccPartSizeFilter
       Dim sPipeGuid As String
       Dim sStructureGuid As String
       Dim oPipeFilter As AeccPartSizeFilter
       Dim oStructureFilter As AeccPartSizeFilter
     
       Debug.Print: Debug.Print
       Debug.Print "PART LIST - "; oPartList.Name
       Debug.Print "-------------------------------------------"
     
       ' From the part list, looking at only those part families
       ' that are pipes, print all the individual parts.
       Debug.Print "  Pipes"
       Debug.Print "  ====="
       For Each oPartFamily In oPartList
          ' Look for only pipe families.
          If (oPartFamily.Domain = aeccDomPipe) Then
             sPipeGuid = oPartFamily.guid
             Debug.Print "  Family: "; oPartFamily.Name
             ' Go through each part in this family.
             For Each oPipeFilter In oPartFamily.SizeFilters
                Debug.Print "    Part: "; oPipeFilter.Name
             Next
          End If
       Next
     
       ' From the part list, looking at only those part families
       ' that are structures, print all the individual parts.
       Debug.Print
       Debug.Print "  Structures"
       Debug.Print "  =========="
       For Each oPartFamily In oPartList
          ' Look for only structure families.
          If (oPartFamily.Domain = aeccDomStructure) Then
             sStructureGuid = oPartFamily.guid
             Debug.Print "  Family: "; oPartFamily.Name
             ' Go through each part in this family.
             For Each oPipeFilter In oPartFamily.SizeFilters
                Debug.Print "    Part: "; oPipeFilter.Name
             Next
          End If
       Next
    Next
