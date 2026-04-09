<!-- Developer's Guide > API Developer's Guide >  .NET Core Developer's Guide > Known Issues in Civil 3D .NET Core Development -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B50CC834-E202-48FE-9C64-526EF9828535.htm -->

# Known Issues in Civil 3D .NET Core Development

## Subassembly Composer Issues after Porting to .NET

In the Subassembly Composer (SAC), the significant impact of .NET is the discontinuation of support for Windows Workflow Foundation assemblies. These are integral to the application's core engine. To ensure continued functionality of SAC subassemblies in Civil 3D, we have implemented the following hybrid solution: 

  * **CoreWF** : The open source porting of the Workflow Foundation runtime is used when PKT files build corridors. 
  * **PKT Design** : PKT file creation continues using the .NET Framework. There is no .NET package or porting for the UI components of the Workflow Foundation. 

Adding to the complexity, CoreWF changes when porting to .NET, notably there is limited visual basic scripting support in Roslyn. In the .NET Framework, compiling VB scripts is swift, whereas in .NET, it requires significantly more time to generate an executable expression from scripts. 

As a reference, we are summarizing the known issues here in Civil 3D 2025. 

  * Workflow running time is slower than before. This should only impact the first execution of a workflow such as creating a subassembly for the first time, or building the first applied station of a corridor. For a moderate corridor, the whole rebuilding time of a moderate corridor is improved. Please note that, open drawing time is not impacted. Specifically, the porting will not impact the loading time of the tool space. 
  * Roslyn has stricter rules for VB script compiling. There may be cases where the designer does not show warnings and displays the subassembly preview, but it still may not run in Civil 3D. For example, if your workflow contains a Condition expression such as: 
        
        AP1.X >=1.0_
        and AP1.Y >=2.0_

Roslyn will expect more text after the ending ' _' and find it invalid. While we have fixed this issue, there could be more undiscovered inconsistency cases. If you discover failures, be sure to review your workflow and identify any possible invalid scripts, or pass the PKT file to us for closer diagnosis. 

## Startup and Runtime Crashes/Exceptions Due to Plugins

Not all crashes/exceptions in plugins are caused by this issue, but it is worth checking the PackageContents.xml file in the subfolders under your plugin folders to ensure that it is properly configured . 

Locations to check include: 

  * C:\ProgramData\Autodesk\ApplicationPlugins 
  * %APPDATA%\Autodesk\ApplicationPlugins 
  * C:\Program Files\Autodesk\ApplicationPlugins 
  * C:\Program Files (x86)\Autodesk\ApplicationPlugins 

For Civil 3D 2025 plugins, be sure to set both SeriesMin and SeriesMax to "R25.0" and Platform to "Civil3D" to ensure it can be loaded and is only loaded in Civil 3D 2025. See more details on [AutoCAD 2024 Developer and ObjectARX Help | Runtime Requirements Element Reference](<https://help.autodesk.com/view/OARX/2024/ENU/?guid=GUID-1591CA01-EF87-48CD-952B-772FE26037F1>)

## Plugin fails to load due to the lack of a framework reference to Microsoft.AspNetCore.App

Civil 3D does not rely on Microsoft.AspNetCore.App, so it has not added this reference. If your plugin has a dependency on it, it may prevent the plugin from running. 

**Solution** : Edit the acdbmgd.runtimeconfig.json file located in the Civil 3D root folder by adding a reference to Microsoft.AspNetCore.App. If you are using a script or installer to add it, incorporate logic to check whether the user or other plugins have already included it before adding it to avoid duplication. Also, ensure that the desired version has been installed by Civil 3D using the "dotnet --list-runtimes" command. Otherwise, you may consider including the framework installer within your plugin installer. 
    
    
    {
      "runtimeOptions": {
        "tfm": "net8.0",
        "frameworks": [
          {
            "name": "Microsoft.NETCore.App",
            "version": "8.0.0"
          },
          {
            "name": "Microsoft.WindowsDesktop.App",
            "version": "8.0.0"
          },
          {
            "name": "Microsoft.AspNetCore.App",
            "version": "8.0.0"
          }
        ],
        "configProperties": {
          "Switch.System.Windows.Controls.ItemsControlDoesNotSupportAutomation": true,
          "System.Reflection.Metadata.MetadataUpdater.IsSupported": false,
          "System.Runtime.Serialization.EnableUnsafeBinaryFormatterSerialization": true
        }
      }
    }
