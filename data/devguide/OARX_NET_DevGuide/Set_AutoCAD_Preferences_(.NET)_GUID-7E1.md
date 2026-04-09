<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Set AutoCAD Preferences (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7E1AC51A-CDD6-4CD5-8703-3D3A472BFFC5.htm -->

# Set AutoCAD Preferences (.NET)

The AutoCAD .NET API does not contain any classes or methods to access the options in which are accessed through the AutoCAD Options dialog box. Access to these options is done through the ActiveX® Automation library. You use the COM object returned from the Preferences property of the Application object. 

Once you have the Preferences COM object, you can then access the nine objects pertaining to the options, each representing a tab in the Options dialog box. These objects provide access to all of the registry-stored options in the Options dialog box. You can customize many of the AutoCAD settings by using properties found on these objects. These objects are 

  * PreferencesDisplay 
  * PreferencesDrafting 
  * PreferencesFiles 
  * PreferencesOpenSave 
  * PreferencesOutput 
  * PreferencesProfiles 
  * PreferencesSelection 
  * PreferencesSystem 
  * PreferencesUser 

## Access the Preferences object

The following example shows how to access the Preferences object through COM interop. 

### C#
    
    
    AcadPreferences acPrefComObj = (AcadPreferences)Application.Preferences;

### VB.NET
    
    
    Dim acPrefComObj As AcadPreferences = Application.Preferences

### VBA/ActiveX Code Reference
    
    
    Dim acadPref as AcadPreferences
    Set acadPref = ThisDrawing.Application.Preferences

After you reference the Preferences object, you can then access any of the specific Preferences objects using the Display, Drafting, Files, OpenSave, Output, Profile, Selection, System, and User properties. 

##  Set the crosshairs to full screen

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Interop;
     
    [CommandMethod("PrefsSetCursor")]
    public static void PrefsSetCursor()
    {
        // This example sets the crosshairs for the drawing window
        // to full screen.
     
        // Access the Preferences object
        AcadPreferences acPrefComObj = (AcadPreferences)Application.Preferences;
     
        // Use the CursorSize property to set the size of the crosshairs
        acPrefComObj.Display.CursorSize = 100;
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Interop
     
    <CommandMethod("PrefsSetCursor")> _
    Public Sub PrefsSetCursor()
        '' This example sets the crosshairs of the AutoCAD drawing cursor
        '' to full screen.
     
        '' Access the Preferences object
        Dim acPrefComObj As AcadPreferences = Application.Preferences
     
        '' Use the CursorSize property to set the size of the crosshairs
        acPrefComObj.Display.CursorSize = 100
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub PrefsSetCursor()
        ' This example sets the crosshairs of the AutoCAD drawing cursor
        ' to full screen
     
        ' Access the Preferences object
        Dim acadPref As AcadPreferences
        Set acadPref = ThisDrawing.Application.Preferences
     
        ' Use the CursorSize property to set the size of the crosshairs
        acadPref.Display.CursorSize = 100
    End Sub

##  Hide the scroll bars

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Interop;
     
    [CommandMethod("PrefsSetDisplay")]
    public static void PrefsSetDisplay()
    {
        // This example disables the scroll bars
     
        // Access the Preferences object
        AcadPreferences acPrefComObj = (AcadPreferences)Application.Preferences;
     
        // Disable the scroll bars
        acPrefComObj.Display.DisplayScrollBars = false;
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Interop
     
    <CommandMethod("PrefsSetDisplay")> _
    Public Sub PrefsSetDisplay()
        '' This example disables the scroll bars
     
        '' Access the Preferences object
        Dim acPrefComObj As AcadPreferences = Application.Preferences
     
        '' Disable the scroll bars
        acPrefComObj.Display.DisplayScrollBars = False
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub PrefsSetDisplay()
        ' This example disables the scroll bars
     
        ' Access the Preferences object
        Dim acadPref As AcadPreferences
        Set acadPref = ThisDrawing.Application.Preferences
     
        ' Disable the scroll bars
        acadPref.Display.DisplayScrollBars = False
    End Sub
