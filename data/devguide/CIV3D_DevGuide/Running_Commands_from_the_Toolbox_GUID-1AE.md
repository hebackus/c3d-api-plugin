<!-- Developer's Guide > API Developer's Guide > Getting Started > Running Commands from the Toolbox -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1AE54A00-E3DB-4B0C-B17E-D49E6D62E700.htm -->

# Running Commands from the Toolbox

The recommended method to expose a Autodesk Civil 3D extension to users is to add it to the Toolbox tab in Toolspace, by creating a toolbox macro. The Toolbox handles loading the .NET assembly or ARX DLL containing the commands. 

There are two execution types that a toolbox macro can have:

  1. CMD - the command name is sent to the command line to execute. This is the recommended execution type for both .NET and ARX commands.
  2. .NET - a method name is located, via Reflection, in the assembly, and is executed directly. No attribute flags are read and the code is always run in application context. (A command executed from the command line runs in the drawing context by default). Therefore, code run as as a .NET execute type must always be a static method, and must handle its own document locking.

Note:

It is safe to explicitly lock a document, even if the code might be run in document context.

Here is an example of how to handle document locking:
    
    
    static void setPrecision()
    {
        using (Autodesk.AutoCAD.ApplicationServices.DocumentLock locker = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.LockDocument())
        {
            // perform any document / database modifications here
            CivilApplication.ActiveDocument.Settings.DrawingSettings.AmbientSettings.Station.Precision.Value = 2;
        }
    }
