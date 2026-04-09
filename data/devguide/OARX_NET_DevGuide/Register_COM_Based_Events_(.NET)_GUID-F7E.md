<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Register COM Based Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F7E86804-F789-418F-937D-919188D88A45.htm -->

# Register COM Based Events (.NET)

The AutoCAD COM Automation library offers some unique events that are not found in the .NET API. Registering events that are in a COM library is different than how you would initialize an event using VB or VBA. You use the VB.NET AddHandler statement or the C# += operator to reigister an event handler with the event. The event handler requires the address of the procedure in which should be called when the event is raised. 

## Register a COM based event

This example demonstrates how to register the BeginFileDrop event using COM interop. The BeginFileDrop event is associated with the Application object of the AutoCAD COM Automation library. Once the commands are loaded into AutoCAD, enter AddCOMEvent at the Command prompt and then drag and drop a DWG file into the drawing window. A message box will be displayed prompting you to continue. Use the RemoveCOMEvent command to remove the event handler. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    using Autodesk.AutoCAD.Interop;
    using Autodesk.AutoCAD.Interop.Common;
     
    // Global variable for AddCOMEvent and RemoveCOMEvent commands
    AcadApplication acAppCom;
     
    [CommandMethod("AddCOMEvent")]
    public void AddCOMEvent()
    {
      // Set the global variable to hold a reference to the application and
      // register the BeginFileDrop COM event
      acAppCom = Application.AcadApplication as AcadApplication;
      acAppCom.BeginFileDrop += 
          new _DAcadApplicationEvents_BeginFileDropEventHandler(appComBeginFileDrop);
    }
     
    [CommandMethod("RemoveCOMEvent")]
    public void RemoveCOMEvent()
    {
      // Unregister the COM event handle
      acAppCom.BeginFileDrop -= 
          new _DAcadApplicationEvents_BeginFileDropEventHandler(appComBeginFileDrop);
      acAppCom = null;
    }
     
    public void appComBeginFileDrop(string strFileName, ref bool bCancel)
    {
      // Display a message box prompting to continue inserting the DWG file
      if (System.Windows.Forms.MessageBox.Show("AutoCAD is about to load " + strFileName +
                                           "\nDo you want to continue loading this file?",
                                           "DWG File Dropped",
                                           System.Windows.Forms.MessageBoxButtons.YesNo) == 
                                           System.Windows.Forms.DialogResult.No)
      {
          bCancel = true;
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    Imports Autodesk.AutoCAD.Interop
    Imports Autodesk.AutoCAD.Interop.Common
     
    '' Global variable for AddCOMEvent and RemoveCOMEvent commands
    Dim acAppCom As AcadApplication
     
    <CommandMethod("AddCOMEvent")> _
    Public Sub AddCOMEvent()
      '' Set the global variable to hold a reference to the application and
      '' register the BeginFileDrop COM event
      acAppCom = Application.AcadApplication
      AddHandler acAppCom.BeginFileDrop, AddressOf appComBeginFileDrop
    End Sub
     
    <CommandMethod("RemoveCOMEvent")> _
    Public Sub RemoveCOMEvent()
      '' Unregister the COM event handle
      RemoveHandler acAppCom.BeginFileDrop, AddressOf appComBeginFileDrop
      acAppCom = Nothing
    End Sub
     
    Public Sub appComBeginFileDrop(ByVal strFileName As String, _
                                   ByRef bCancel As Boolean)
      '' Display a message box prompting to continue inserting the DWG file
      If System.Windows.Forms.MessageBox.Show("AutoCAD is about to load " & _
                              strFileName & vbLf & _
                              "Do you want to continue loading this file?", _
                              "DWG File Dropped", _
                              System.Windows.Forms.MessageBoxButtons.YesNo) = _
        System.Windows.Forms.DialogResult.No Then
          bCancel = True
      End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Public WithEvents ACADApp As AcadApplication
    
    Sub Example_AcadApplication_Events()
        ' Intialize the public variable (ACADApp)
        ' which will be used to intercept AcadApplication Events
        '
        ' Run this procedure FIRST!
        Set ACADApp = ThisDrawing.Application
    End Sub
    
    Private Sub ACADApp_BeginFileDrop _
     (ByVal FileName As String, Cancel As Boolean)
        ' This procedure intercepts an Application BeginFileDrop event.
        '
        ' This event is triggered when a drawing file is dragged
        ' into AutoCAD.
        '
        ' To trigger this example event:
        '     1) Run the Example_AcadApplication_Events procedure to initialize
        '     the public variable (named ACADApp) linked to this event.
        '
        '     2) Drag an AutoCAD drawing file into the AutoCAD
        '        application from either the Windows Desktop
        '        or Windows Explorer
        '
        ' Use the "Cancel" variable to stop the loading of the
        ' dragged file, and the "FileName" variable to  notify
        ' the user which file is about to be dragged in.
     
        If MsgBox("AutoCAD is about to load " & FileName & vbCrLf _
                  & "Do you want to continue loading this file?", _
                  vbYesNoCancel + vbQuestion) <> vbYes Then
            Cancel = True
        End If
    End Sub
