<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Work with Raster Images (.NET) > Manage Raster Images (.NET) > Change Image File Paths (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-475A8D8C-61A3-4C72-849A-D2FB39C4C9D9.htm -->

# Change Image File Paths (.NET)

The path and file name of an image is queried or changed using the SourceFileName property of the RasterImageDef object assigned to a RasterImage object. The path set by this property is the actual path where AutoCAD looks for the image. 

If AutoCAD cannot locate the drawing (for example, if you have moved the file to a different directory than the one saved with the SourceFileName property), it removes relative or absolute path information from the name (for example, _\images\tree.tga_ or _c:\my project\images\tree.tga_ becomes _tree.tga_) and searches the paths you have defined using the SetProjectFilePath method on the Preferences object. If the file is not located in the paths, it attempts the first search path again. If AutoCAD locates and loads the image file, ActiveFileName property is updated to reflect the location the file was found at. 

You can remove the path from the file name or specify a relative path by resetting the SourceFileName property. 

Changing the path in the SourceFileName property does not affect the project files' search-path settings.
