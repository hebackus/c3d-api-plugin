<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Distribute Your Application (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-70D60274-57E0-4B22-8D0C-3C7F212A7CAF.htm -->

# Distribute Your Application (.NET)

.NET applications can be distributed in two deployable builds: debug and release. 

  * **Debug build** \- Contains debugging related information. .NET assemblies containing debug information are larger in size than a Release build of a .NET assembly. 
  * **Release build** \- Contains no debug related information. 

You must choose the type of build to distribute your application in, both build types can be loaded into AutoCAD. Debug builds are usually only used when developing and testing an application, while a Release build is built when you are distributing an application for use on many computers inside or outside of your company. 

## To generate a Release build for a .NET assembly

The following steps explain how to generate a Release build of a .NET assembly. 

  1. In Microsoft Visual Studio, open the project you want to generate a Release build for. 
  2. Click Build menu  Configuration Manager. 
  3. In the Configuration Manager, Active Solution Configuration drop-down list, select Release. 
  4. Click Close. 
  5. In Microsoft Visual Studio, click Build menu  Build Solution. 

## Load a .NET assembly

After you have determined the build type of your .NET assembly, you must determine how it will be loaded into AutoCAD. A .NET assembly file can be loaded manually or with demand loading. 

  * **Manually** \- Use the NETLOAD command at the Command prompt or within an AutoLISP file. 
  * **Demand load** \- Define a key specific to the application you want to load when AutoCAD starts up. The key must be placed under the Application key for the specific release of AutoCAD that you want your application to be loaded in. 

The key for the application can contain the following keys: 

DESCRIPTION
    

Description of the .NET assembly and is optional. 

LOADCTRLS
    

Controls how and when the .NET assembly is loaded. 

    * 1 - Load application upon detection of proxy object 
    * 2 - Load the application at startup 
    * 4 - Load the application at start of a command 
    * 8 - Load the application at the request of a user or another application 
    * 16 - Do not load the application 
    * 32 - Load the application transparently 
LOADER
    

Specifies which .NET assembly file to load. 

MANAGED
    

Specifies the file that should be loaded is a .NET assembly or ObjectARX file. Set to 1 for .NET assembly files. 

## Demand load a .NET application

The following examples create and remove the required keys in the registry to load a .NET assembly file at the startup of AutoCAD. When the RegisterMyApp command is used, the required registry keys are created that will automatically load the application the next time AutoCAD starts. The UnregisterMyApp command removes the demand loading information from the registry so the application is not loaded the next time AutoCAD starts. 

### C#
    
    
    using Microsoft.Win32;
    using System.Reflection;
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    
    [CommandMethod("RegisterMyApp")]
    public void RegisterMyApp()
    {
      // Get the AutoCAD Applications key
      string sProdKey = HostApplicationServices.Current.RegistryProductRootKey;
      string sAppName = "MyApp";
    
      RegistryKey regAcadProdKey = Registry.CurrentUser.OpenSubKey(sProdKey);
      RegistryKey regAcadAppKey = regAcadProdKey.OpenSubKey("Applications", true);
    
      // Check to see if the "MyApp" key exists
      string[] subKeys = regAcadAppKey.GetSubKeyNames();
      foreach (string subKey in subKeys)
      {
          // If the application is already registered, exit
          if (subKey.Equals(sAppName))
          {
              regAcadAppKey.Close();
              return;
          }
      }
    
      // Get the location of this module
      string sAssemblyPath = Assembly.GetExecutingAssembly().Location;
    
      // Register the application
      RegistryKey regAppAddInKey = regAcadAppKey.CreateSubKey(sAppName);
      regAppAddInKey.SetValue("DESCRIPTION", sAppName, RegistryValueKind.String);
      regAppAddInKey.SetValue("LOADCTRLS", 14, RegistryValueKind.DWord);
      regAppAddInKey.SetValue("LOADER", sAssemblyPath, RegistryValueKind.String);
      regAppAddInKey.SetValue("MANAGED", 1, RegistryValueKind.DWord);
    
      regAcadAppKey.Close();
    }
    
    [CommandMethod("UnregisterMyApp")]
    public void UnregisterMyApp()
    {
      // Get the AutoCAD Applications key
      string sProdKey = HostApplicationServices.Current.RegistryProductRootKey;
      string sAppName = "MyApp";
    
      RegistryKey regAcadProdKey = Registry.CurrentUser.OpenSubKey(sProdKey);
      RegistryKey regAcadAppKey = regAcadProdKey.OpenSubKey("Applications", true);
    
      // Delete the key for the application
      regAcadAppKey.DeleteSubKeyTree(sAppName);
      regAcadAppKey.Close();
    }

### VB.NET
    
    
    Imports Microsoft.Win32
    Imports System.Reflection
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    
    <CommandMethod("RegisterMyApp")> _
    Public Sub RegisterMyApp()
      '' Get the AutoCAD Applications key
      Dim sProdKey As String = HostApplicationServices.Current.RegistryProductRootKey
      Dim sAppName As String = "MyApp"
    
      Dim regAcadProdKey As RegistryKey = Registry.CurrentUser.OpenSubKey(sProdKey)
      Dim regAcadAppKey As RegistryKey = regAcadProdKey.OpenSubKey("Applications", True)
    
      '' Check to see if the "MyApp" key exists
      Dim subKeys() As String = regAcadAppKey.GetSubKeyNames()
      For Each sSubKey As String In subKeys
          '' If the application is already registered, exit
          If (sSubKey.Equals(sAppName)) Then
              regAcadAppKey.Close()
    
              Exit Sub
          End If
      Next
    
      '' Get the location of this module
      Dim sAssemblyPath As String = Assembly.GetExecutingAssembly().Location
    
      '' Register the application
      Dim regAppAddInKey As RegistryKey = regAcadAppKey.CreateSubKey(sAppName)
      regAppAddInKey.SetValue("DESCRIPTION", sAppName, RegistryValueKind.String)
      regAppAddInKey.SetValue("LOADCTRLS", 14, RegistryValueKind.DWord)
      regAppAddInKey.SetValue("LOADER", sAssemblyPath, RegistryValueKind.String)
      regAppAddInKey.SetValue("MANAGED", 1, RegistryValueKind.DWord)
    
      regAcadAppKey.Close()
    End Sub
    
    <CommandMethod("UnregisterMyApp")> _
    Public Sub UnregisterMyApp()
      '' Get the AutoCAD Applications key
      Dim sProdKey As String = HostApplicationServices.Current.RegistryProductRootKey
      Dim sAppName As String = "MyApp"
    
      Dim regAcadProdKey As RegistryKey = Registry.CurrentUser.OpenSubKey(sProdKey)
      Dim regAcadAppKey As RegistryKey = regAcadProdKey.OpenSubKey("Applications", True)
    
      '' Delete the key for the application
      regAcadAppKey.DeleteSubKeyTree(sAppName)
      regAcadAppKey.Close()
    End Sub
