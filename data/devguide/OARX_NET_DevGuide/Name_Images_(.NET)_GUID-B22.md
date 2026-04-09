<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Work with Raster Images (.NET) > Manage Raster Images (.NET) > Name Images (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B2275251-B262-4607-BDBE-7A73200E8744.htm -->

# Name Images (.NET)

Image names are not necessarily the same as image file names. When you attach an image to a drawing, you assign a name to the image file reference in the Image dictionary. You can change the image name without affecting the name of the file. 

The image file is represented by the SourceFileName property on the RasterImageDef object. Changing the SourceFileName property will change the image in the drawing. The image name is represented by the Key property for the DBDictionaryEntry object that represents the RasterImageDef object, and changing the Key property will change the name of the image only, not the file associated with it.
