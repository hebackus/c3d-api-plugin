<!-- Developer's Guide > API Developer's Guide >  .NET Core Developer's Guide > Creating New Civil 3D .NET Plugins > Add Library References in the Reference Manager -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-267E68C8-AD2D-4F7F-87DF-831018D56CDB.htm -->

# Add Library References in the Reference Manager

Set the target framework to .NET 8.0 and create the project. 

  1. Invoke the Reference Manager in one of two ways: 
     * Select Project menu  Add Project Reference/ Add COM Reference. 
     * Right-click Dependencies in the Solution Explorer and select Add Project Reference/ Add COM Reference. 
  2. Navigate to the installation directory of Autodesk Civil 3D and choose the following base libraries: AcDbMgd.dll, AcMgd.dll, AcCoreMgd.dll, AecBaseMgd.dll, and AeccDbMgd.dll. 

Note: These are the base AutoCAD and Autodesk Civil 3D managed libraries. Your .NET assembly can use classes defined in additional libraries. 

  3. To allow debugging and reduce the disk space requirements for your projects, select these libraries in the Visual Studio Solution Explorer, and set the Copy Local property to False.
