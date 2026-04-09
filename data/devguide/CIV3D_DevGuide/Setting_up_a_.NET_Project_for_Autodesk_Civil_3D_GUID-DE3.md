<!-- Developer's Guide > API Developer's Guide > Getting Started > Setting up a .NET Project for Autodesk Civil 3D -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DE3A46DA-508E-43A0-8538-C77D978D06B2.htm -->

# Setting up a .NET Project for Autodesk Civil 3D

This section describes the basic steps to set up a .NET solution using Visual Studio and the Autodesk Civil 3D managed classes. The steps are the similar whether you use Microsoft Visual C# .NET or Visual Basic .NET. The example below uses C# in Visual Studio 2010. Express (free) versions of Visual Studio may look slightly different, but can also be used. 

To create a new project that uses the Autodesk Civil 3D managed classes in Microsoft Visual Studio

  1. In Visual Studio 2010, create a new class library solution and project. 

New Project Dialog in Visual Studio 

  2. Select Project menu Add References, or right-click References in the Solution Explorer and select Add References. 
  3. Browse to the install directory for Autodesk Civil 3D, and select the base libraries acdbmgd.dll, acmgd.dll, accoremgd.dll, AecBaseMgd.dll, and AeccDbMgd.dll. 

Note:

These are the base AutoCAD and Autodesk Civil 3D managed libraries. Your .NET assembly can use classes defined in additional libraries. 

To allow debugging and reduce the disk space requirements for your projects, select these libraries in the Visual Studio Solution Explorer, and set the Copy Local property to **False**. 

  4. Optionally, you can configure your project to start Autodesk Civil 3D when you run the application from Visual Studio, which is useful for debugging. 

Note:

This option is not avaiable in Express (free) versions of Visual Studio. 

     1. On the project Properties page, select the Debug panel. 
     2. Under Start Action, choose Start external program, and enter the path to the acad.exe executable in the Autodesk Civil 3D directory. 
     3. Under Start Options, fill in the Command line arguments: /ld "C:\Program Files\Autodesk Civil 3D 2026\AecBase.dbx" /p "<<C3D_Imperial>>"
     4. Under Start Options, fill in the Working directory, for example: C:\Program Files\Autodesk Civil 3D 2026\UserDataCache\
  5. Implement the IExtensionApplication interface in your main class. Add the Autodesk.AutoCAD.Runtime namespace (which is where this interface is defined), and IExtensionApplication after your class definition: Visual Studio will provide a code complete option to implement stubs for the interface. Your code should now look like this: 
         
         using System;
         using Autodesk.AutoCAD.Runtime;
          
         namespace GettingStarted
         {
             public class Class1 : IExtensionApplication
             {
                 #region IExtensionApplication Members
          
                 public void Initialize()
                 {
                     throw new System.Exception("The method or operation is not implemented.");
                 }
          
                 public void Terminate()
                 {
                     throw new System.Exception("The method or operation is not implemented.");
                 }
          
                 #endregion
             }
         }
         

You can remove or comment out the default content of these methods. Initialize() is called when your assembly is first loaded by a **NETLOAD** command in Autodesk Civil 3D, and can be used for setting up resources, reading configuration files, and other initialization tasks. Terminate() is called when Autodesk Civil 3D shuts down (there is no **NETUNLOAD** command to unload .NET assemblies), and can be used for cleanup to free resources. 

  6. You are now ready to create a public method that is the target of a CommandMethod attribute. This attribute defines the Autodesk Civil 3D command that invokes the method. For example: 
         
         [CommandMethod("HelloWorld")]
         public void HelloWorld()
         {
          
         }
         

  7. Let’s make the method print out a “Hello World” message on the command line. Add the Autodesk.AutoCAD.ApplicationServices namespace, and add this line to the HelloWorld() method: 
         
         Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("\nHello World!\n");
         

You can now build the assembly and run it. Start Autodesk Civil 3D, and type **NETLOAD** at the command line. In the Choose .NET Assembly dialog, browse to your assembly DLL (if you are using the project settings from step 1, this will be GettingStarted.dll). Type **HELLOWORLD** at the command line, and you will see the command output: 

  8. The previous step used functionality from the AutoCAD Application class. Let’s include some functionality specific to the Autodesk Civil 3D managed classes. First, add two more namespaces: Autodesk.AutoCAD.DatabaseServices and Autodesk.Civil.ApplicationServices. Then add these lines to obtain the current Civil document, get some basic information about it, and print the information out: 
         
         public void HelloWorld()
         {
             CivilDocument doc = Autodesk.Civil.ApplicationServices.CivilApplication.ActiveDocument;
             ObjectIdCollection alignments = doc.GetAlignmentIds();
             ObjectIdCollection sites = doc.GetSiteIds();
             String docInfo = String.Format("\nHello World!\nThis document has {0} alignments and {1} sites.\n", alignments.Count, sites.Count);
             Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(docInfo);
          
         }
         

Open or create a document in Autodesk Civil 3D that contains alignments and sites. When you run the **HELLOWORLD** command now, you should see output similar to this: 

For more samples, look in the Autodesk Civil 3D\samples\dotNet directory.
