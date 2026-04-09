<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Profiles in COM > Profiles > Editing Points of Vertical Intersection -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-41C584BC-B38A-40C2-A055-EEAFFF8C3BEA.htm -->

# Editing Points of Vertical Intersection

The point where two adjacent tangents would cross (whether they actually cross or not) is called the “point of vertical intersection”, or “PVI.” This location can be useful for editing the geometry of a profile because this one point controls the slopes of both tangents and any curve connecting them. The collection of all PVIs in a profile are contained in the AeccProfile.PVIs property. This object lets you access, add, and remove PVIs from a profile, which can change the position and number of entities that make up the profile. Individual PVIs (type AeccProfilePVI) do not have a name or id, but are instead identified by a particular station and elevation. The collection methods AeccProfilePVIs.ItemAt and AeccProfilePVIs.RemoveAt access or delete the PVI closest to the station and elevation parameters so you do not need the exact location of the PVI you want to modify.

This sample identifies the PVI closest to a specified point. It then adds a new PVI to profile created in the [Creating a Profile Using Entities](<GUID-409176A7-99F7-462A-A2E0-30449957CAB6.htm>) topic and adjusts its elevation.
    
    
    Dim oPVI As AeccProfilePVI
     
    ' Find the PVI close to station 1000 elevation -70.
    Set oPVI = Nothing
    Set oPVI = oProfile.PVIs.ItemAt(1000, -70)
    Debug.Print "PVI closest to station 1000 is at station: "; 
    Debug.Print oPVI.Station
     
    ' Add another PVI and slightly adjust its elevation.
    Set oPVI = oProfile.PVIs.Add(607.4, -64.3, aeccProfileTangent)
    oPVI.Elevation = oPVI.Elevation - 2#
