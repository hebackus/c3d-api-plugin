<!-- Developer's Guide > API Developer's Guide >  .NET Core Developer's Guide > Creating New Civil 3D .NET Plugins > Add Functionality Code and Build the Assembly -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0ACBC30C-B5C0-4004-8476-A0EB49767990.htm -->

# Add Functionality Code and Build the Assembly

  * Add [assembly: ExtensionApplication(C3D_Plugin.C3D_Plugin)][assembly: CommandClass(C3D_Plugin.C3D_Plugin)] for better DLL loading performance by avoiding scanning all exported types. 
  * Implement the IExtensionApplication interface in your main class. 
  * Create a public method that is the target of a CommandMethod 

##  Civil 3D plugin sample code 
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.ApplicationServices.Core;
      
    using Autodesk.Civil.ApplicationServices;
    [assembly: ExtensionApplication(C3D_Plugin.C3D_Plugin)]
    [assembly: CommandClass(C3D_Plugin.C3D_Plugin)] 
    namespace C3D_Plugin
    {
        public class C3D_Plugin : IExtensionApplication
        {
            public void Initialize()
            {
            }
      
            public void Terminate()
            {
            }
      
            [CommandMethod("HelloCivil3D")]
            public void HelloCivil3D()
            {           
                Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("\nHello Civil 3D! It's a Civil 3D plugin.\n");
      
                CivilDocument doc = CivilApplication.ActiveDocument;
                ObjectIdCollection alignments = doc.GetAlignmentIds();
                ObjectIdCollection sites = doc.GetSiteIds();
                string docInfo = string.Format("\nThis document has {0} alignments and {1} sites.\n", alignments.Count, sites.Count);
                Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(docInfo);
            }
        }
    }

Note:

  * **.Initialize()** is called when your assembly is first loaded by a NETLOAD command in Autodesk Civil 3D, and can be used for setting up resources, reading configuration files, and other initialization tasks. 
  * **Terminate()** i s called when Autodesk Civil 3D shuts down (there is no NETUNLOAD command to unload .NET assemblies), and can be used for cleanup to free resources. 
  * **CommandMethodattribute** defines the Autodesk Civil 3D command that invokes the method. 

Now you should build the assembly
