<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Register and Unregister Events (.NET) > Handle Application Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4BD5D384-5448-4D19-9023-DA12A55FAEF0.htm -->

# Handle Application Events (.NET)

Application object events are used to respond to the application window. Once an Application event is registered, it remains registered until AutoCAD is shutdown or the event is unregistered. 

The following events are available for the Application object: 

BeginCustomizationMode
    

Triggered just before AutoCAD enters customization mode. 

BeginDoubleClick
    

Triggered when the mouse button is double clicked. 

BeginQuit
    

Triggered just before an AutoCAD session ends. 

DisplayingCustomizeDialog
    

Triggered just before the Customize dialog box is displayed. 

DisplayingDraftingSettingsDialog
    

Triggered just before the Drafting Settings dialog box is displayed. 

DisplayingOptionDialog
    

Triggered just before the Options dialog box is displayed. 

EndCustomizationMode
    

Triggered when AutoCAD exits customization mode. 

EnterModal
    

Triggered just before a modal dialog box is displayed. 

Idle
    

Triggered when AutoCAD text. 

LeaveModal
    

Triggered when a modal dialog box is closed. 

PreTranslateMessage
    

Triggered just before a message is translated by AutoCAD. 

QuitAborted
    

Triggered when an attempt to shutdown AutoCAD is aborted. 

QuitWillStart
    

Triggered after the BeginQuit event and before shutdown begins. 

SystemVariableChanged
    

Triggered when an attempt to change a system variable is made. 

SystemVariableChanging
    

Triggered just before an attempt is made at changing a system variable. 

## Enable an Application object event

This example demonstrates how to register an event handler with the BeginQuit event. Once registered, a message box is displayed before AutoCAD completely shutdown. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    [CommandMethod("AddAppEvent")]
    public void AddAppEvent()
    {
      Application.SystemVariableChanged +=
          new Autodesk.AutoCAD.ApplicationServices.
              SystemVariableChangedEventHandler(appSysVarChanged);
    }
     
    [CommandMethod("RemoveAppEvent")]
    public void RemoveAppEvent()
    {
      Application.SystemVariableChanged -=
          new Autodesk.AutoCAD.ApplicationServices.
              SystemVariableChangedEventHandler(appSysVarChanged);
    }
     
    public void appSysVarChanged(object senderObj, 
                                 Autodesk.AutoCAD.ApplicationServices.
                                 SystemVariableChangedEventArgs sysVarChEvtArgs)
    {
      object oVal = Application.GetSystemVariable(sysVarChEvtArgs.Name);
     
      // Display a message box with the system variable name and the new value
      Application.ShowAlertDialog(sysVarChEvtArgs.Name + " was changed." +
                                  "\nNew value: " + oVal.ToString());
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
     
    <CommandMethod("AddAppEvent")> _
    Public Sub AddAppEvent()
      AddHandler Application.SystemVariableChanged, AddressOf appSysVarChanged
    End Sub
     
    <CommandMethod("RemoveAppEvent")> _
    Public Sub RemoveAppEvent()
      RemoveHandler Application.SystemVariableChanged, AddressOf appSysVarChanged
    End Sub
     
    Public Sub appSysVarChanged(ByVal senderObj As Object, _
                                ByVal sysVarChEvtArgs As Autodesk.AutoCAD.ApplicationServices. _
                                SystemVariableChangedEventArgs)
     
      Dim oVal As Object = Application.GetSystemVariable(sysVarChEvtArgs.Name)
     
      '' Display a message box with the system variable name and the new value
      Application.ShowAlertDialog(sysVarChEvtArgs.Name & " was changed." & _
                                  vbLf & "New value: " & oVal.ToString())
    End Sub

### VBA/ActiveX Code Reference
    
    
    Public WithEvents ACADApp As AcadApplication
     
    Sub Example_AcadApplication_Events()
        ' Intialize the public variable (ACADApp)
        '
        ' Run this procedure first
     
        Set ACADApp = ThisDrawing.Application
    End Sub
     
    Private Sub ACADApp_SysVarChanged(ByVal SysvarName As String, _
                                      ByVal newVal As Variant)
        ' This procedure intercepts an Application SysVarChanged event.
     
        MsgBox (SysvarName & " was changed." & _
                vbLf & "New value: " & newVal)
    End Sub
