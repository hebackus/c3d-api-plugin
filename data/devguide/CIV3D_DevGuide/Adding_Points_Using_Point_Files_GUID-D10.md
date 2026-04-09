<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with TIN Surfaces > Adding Point Data to a TIN Surface > Adding Points Using Point Files -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D1077E58-F4DC-45E2-A942-F2CCA2AC7F49.htm -->

# Adding Points Using Point Files

The AeccTinSurface.PointFiles collection contains the names of text files that contain point information. These text files must consist only of lines containing the point number, easting, northing, and elevation delineated by spaces. Except for comment lines beginning with “#”, any other information will result in an error. Unlike TIN or LandXML files, text files do not contain a list of faces - the points are automatically joined into a series of triangles based on the settings of the AeccTinSurface.DefinitionProperties property.
    
    
    ' Add points from a .txt file to an existing TIN surface.
    sFileName = "C:\My Documents\points.txt"
    oTinSurface.PointFiles.Add sFileName
