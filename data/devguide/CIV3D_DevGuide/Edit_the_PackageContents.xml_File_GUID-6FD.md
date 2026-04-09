<!-- Developer's Guide > API Developer's Guide >  .NET Core Developer's Guide > Creating New Civil 3D .NET Plugins > Edit the PackageContents.xml File -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6FDC9D3D-FAB2-453E-A7BF-F1CC82F4AE18.htm -->

# Edit the PackageContents.xml File

In your PackageContents.xml file, be sure to set both SeriesMin and SeriesMax to "R25.0" and Platform to "Civil3D" to ensure that it can be loaded and only loaded in Civil 3D 2025. 
    
    
    <RuntimeRequirements SeriesMin="R25.0" SeriesMax="R25.0" Platform="Civil3D" OS="Win64"/>

Note: The release date is 2025 in this example. Use appropriate Civil 3D versions as applicable.
