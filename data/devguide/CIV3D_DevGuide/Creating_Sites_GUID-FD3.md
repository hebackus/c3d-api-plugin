<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Sites > Creating Sites -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FD3A9CC1-6CC2-4009-BD77-44CA779EFF77.htm -->

# Creating Sites

All sites in a document are held in the AeccDocument.Sites collection, an object of type AeccSites. The AeccSites.Add method creates a new empty site with the specified name.
    
    
    ' Create a new site.
    Dim oSites As AeccSites
    Set oSites = oAeccDocument.Sites
    Dim oSite As AeccSite
    Set oSite = oSites.Add("Sample Site")
