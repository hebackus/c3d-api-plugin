<!-- Developer's Guide > API Developer's Guide > About the Developer's Guide >   Autodesk Civil 3D APIs -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1FC5774A-14EB-48CC-8A0A-FA983E8B9703.htm -->

#  Autodesk Civil 3D APIs

There are three APIs available for customizing Autodesk Civil 3D: 

  * .NET API — allows you to write extensions to Autodesk Civil 3D in any .NET language. In general, the Autodesk Civil 3D.NET API performs significantly faster than the COM API. Development requires Microsoft Visual Studio 2008 SP1 or better. 
  * COM API — you can create clients that access the COM API from managed (.NET) or unmanaged (C++) code. See [Creating Client Applications](<GUID-5A5D232A-F223-4C3B-9909-00730FB70FA0.htm>). In addition, this API can be used in the Visual Basic for Applications (VBA) IDE, which is available as a separate download. VBA support is deprecated. 
  * Custom Draw API (in C++) — an extension of the AutoCAD ObjectARX API that allows you to customize the way Autodesk Civil 3D renders objects. Development requires Microsoft Visual Studio. 

The COM and .NET APIs are described in this guide. For more information about the Custom Draw API, see the Custom Draw API Reference (civildraw-reference.chm). 

In addition, an API is provided for creating custom subassemblies in .NET. See [Creating Custom Subassemblies Using .NET](<GUID-E295BF67-F60C-49D3-A918-329D1E4FAFC5.htm>). 

Which API you choose to use depends on what you want to do: 

If you want to:  | Use:   
---|---  
Customize the way objects are rendered in Autodesk Civil 3D | the Custom Draw API. The Custom Draw API is an extension of the AutoCAD ObjectARX API. For example, if you wanted to number the triangles on a TIN surface, you could create a DLL using the Custom Draw API. See the sample applications shipped with Autodesk Civil 3D for an example.   
Create macros to automate repetitive actions  | .NET or COM API.   
Create applications to manipulate Autodesk Civil 3D objects  | .NET or COM API.   
  
Note:

Where possible, you should use the Civil .NET API instead of the COM API, especially for longer operations, as the .NET API is a thin layer to Civil objects and has better performance. However, you may find you need to use the COM object to access some functionality or object members that are not yet exposed by the .NET API. In this case it's possible to use both. See [Limitations and Using Interop](<GUID-DD447A5A-DF8B-4905-8BFC-4CBFA1C7C121.htm>) .
