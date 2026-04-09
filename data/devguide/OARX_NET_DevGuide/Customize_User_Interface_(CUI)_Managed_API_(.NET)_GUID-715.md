<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-71554E76-8FD5-4853-82CD-3587764CBCAC.htm -->

# Customize User Interface (CUI) Managed API (.NET)

Many of the user interface elements can be customized in the AutoCAD program with the Customize User Interface (CUI) dialog box or CUI managed API. 

The Customize User Interface (CUI) dialog box allows a user to interactively create and modify many of the user interface elements displayed in the AutoCAD drawing environment, while the CUI managed API can be used by developers to customize the user interface at any time. 

You can use the CUI managed API with these types of applications: 

  * **Plug-in application.** Application that runs within the AutoCAD application environment and leverages AutoCAD system variables and other runtime APIs. A plug-in can make changes to any aspect of the AutoCAD user interface including workspaces, toolbars, menus and shortcuts, though most changes will not take place immediately. 
  * **Stand-alone application.** Application that utilizes the API, but does not need access to any AutoCAD-specific data. For example, an application that does not need to read or write data to a system variable or post a message to the AutoCAD command line. 

See “About User Interface Customization” in the AutoCAD help system for an overview of the user interface, customization files, and element hierarchy. 

## Getting Started

The CUI managed API provides an interface for creating and manipulating the CUIx files, and it does not require AutoCAD to be running. However, when the API is used outside of the AutoCAD program, your program won't have access to the AutoCAD runtime data or other runtime APIs. 

Without access to AutoCAD system variables, accessing AutoCADs main and enterprise CUIx files can be tricky. The main file is generally placed in the _C:\Documents and Settings\ <users profile>\Application Data\Autodesk\AutoCAD <release>\<version>\<language>\Support_ folder. Hard-coding the location of a CUIx file will cause problems when upgrading or when users specify non-default paths for their customization files. 

The _AcCui.dll_ file contains the CUI managed API and is located in the AutoCAD install directory. After referencing the _AcCui.dll_ file to a project, import the Autodesk.AutoCAD.Customization namespace to access the classes of the API. 

For information on referencing library files of the AutoCAD Managed API, see "Components of the AutoCAD .NET API (.NET)." 

## Load a CUIx File

An existing CUIx file must be loaded by passing the full path and file name to the constructor of CustomizationSection class. This parses the file and populates the object with the current interface elements. The MenuGroup contains most of this data within collections. 

When creating a .NET plug-in, the full path to the main AutoCAD CUIx file can be retrieved from the MENUNAME system variable. Since this system variable returns the file name without an extension, the .cuix extension must be added to the return string explicitly. In addition to the main CUIx file, an optional enterprise menu can be loaded. The name of the loaded enterprise menu CUIx file can be accessed from the ENTERPRISEMENU system variable. When no enterprise menu CUIx file is loaded, the value "." is assigned to the ENTERPRISEMENU system variable. 

The following examples demonstrate how to get the full path of the main CUIx file. 

### C#
    
    
    string sMainCuiFile = (string)Application.GetSystemVariable("MENUNAME");
    sMainCuiFile += ".cuix";
    CustomizationSection oCs = new CustomizationSection(sMainCuiFile);

### VB.NET
    
    
    Dim sMainCuiFile As String = Application.GetSystemVariable("MENUNAME")
    sMainCuiFile = sMainCuiFile & ".cuix"
    Dim oCs As CustomizationSection = New CustomizationSection(sMainCuiFile)

## Load a Partial CUIx File

Partial CUIx files are a useful extension to the main or enterprise CUIx files. These can be loaded with the _PartialCUIFiles_ collection in the customization section. This collection provides the full path and file name, with the _.cuix_ extension. When loading partial CUIx files, the application evaluates the entry from the PartialCUIFileCollection, to ensure the full path of the file is being used. 

It is best to add and remove toolbars and menus from partial CUIx files to maintain a separation of your application’s customizations. Define a unique menu group in your partial CUIx files to avoid naming conflicts with other menu groups. The default group in the main CUIx file is “ACAD.”
