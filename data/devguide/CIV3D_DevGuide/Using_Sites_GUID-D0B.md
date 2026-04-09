<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Sites > Using Sites -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D0B5D81A-79FB-4495-B748-B08CCAC0D7DE.htm -->

# Using Sites

A site represents a distinct group of alignments and parcels. Besides containing collections of parcels and alignments, the AeccSite object also contains properties describing how the site objects are numbered and displayed.
    
    
    ' NextAutoCounterParcel sets the starting identification
    ' number for newly created parcels.  The first parcel
    ' created from parcel segments will be 300, the next 301,
    ' and so on.
    oSite.NextAutoCounterParcel = 300
