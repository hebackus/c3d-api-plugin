<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use External References (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-563BAE97-48B1-4DCE-9DDA-16D8C6F13E23.htm -->

# Use External References (.NET)

An external reference (xref) links another drawing to the current drawing. When you insert a drawing as a block, the block and all of the associated geometry is stored in the current drawing database. It is not updated if the original drawing changes. When you insert a drawing as an xref, however, the xref is updated when the original drawing changes. A drawing that contains xrefs, therefore, always reflects the most current editing of each externally referenced file. 

Like a block reference, an xref is displayed in the current drawing as a single object. However, an xref does not significantly increase the file size of the current drawing and cannot be exploded. As with blocks, you can nest xrefs that are attached to your drawing. 

For more information about xrefs, see “About Attaching and Detaching Referenced Drawings (Xrefs)” in the product Help system.
