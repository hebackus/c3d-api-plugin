<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > About .NET and the AutoCAD .NET API (.NET) > Overview of Microsoft Visual Studio (.NET) > C++ Interoperability (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FE481D64-4239-448A-8711-6F6F98D1B092.htm -->

# C++ Interoperability (.NET)

Your .NET application can include C++ portions, so you can also use ObjectARX APIs that do not have managed wrappers. The ObjectARX managed wrapper classes have a consistent property and method that enable you to go back and forth between the managed and unmanaged object. 

A pointer to the underlying unmanaged object from a managed object can be obtained using the UnmanagedObject property. You can create a managed object from an unmanaged object with the DisposableWrapper.Create() method.
