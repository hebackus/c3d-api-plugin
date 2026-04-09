<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Work with Raster Images (.NET) > Modify Images and Image Boundaries (.NET) > Show and Hide Image Boundaries (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-530C64AD-A003-4489-A6F8-0AE907B9EC69.htm -->

# Show and Hide Image Boundaries (.NET)

Hiding an image boundary ensures that the image cannot accidentally be moved or modified and prevents the boundary from being plotted or displayed. When image boundaries are hidden, clipped images are still displayed to their specified boundary limits; only the boundary is affected. Showing and hiding image boundaries affects all images attached to your drawing. 

Use the IsClipped property when you want to show or hide the image boundary. 

Note: This property affects only the image boundary. To see a change in the image when toggling this property, look closely at the small boundary surrounding the image.
