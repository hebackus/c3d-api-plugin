<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Baselines > Adding a Baseline to a Corridor -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A984B0D2-B596-4013-8AAD-98759088C6BF.htm -->

# Adding a Baseline to a Corridor

A baseline can be added to an existing corridor through the AeccCorridor.AddBaseline method. The baseline is defined by an existing alignment, profile, and assembly and consists of a single region.

Note:

The station distance between assemblies cannot be set through the API, and needs to be set through the property page dialog box before this method is called.

The following sample adds a baseline using an existing alignment, profile, and assembly:
    
    
    Set oBaseline = oCorridor.AddBaseline _
       (oAlignment.Name, oProfile.Name, oAssembly.Name)
