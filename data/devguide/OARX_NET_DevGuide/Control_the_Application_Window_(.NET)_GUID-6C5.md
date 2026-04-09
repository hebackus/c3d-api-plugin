<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Application Window (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-6C52F8BC-B107-4EE4-BA25-5B74900B271A.htm -->

# Control the Application Window (.NET)

The ability to control the Application window allows developers the flexibility to create effective and intelligent applications. There will be times when it is appropriate for your application to minimize the AutoCAD window, perhaps while your code is performing work in another application such as Microsoft® Excel®. Additionally, you will often want to verify the state of the AutoCAD window before performing such tasks as prompting for input from the user. 

Using methods and properties found on the Application object, you can change the position, size, and visibility of the Application window. You can also use the WindowState property to minimize, maximize, and check the current state of the Application window. 

## Position and size the Application window

This example uses the Location and Size properties to position the AutoCAD Application window in the upper-left corner of the screen and size it to 400 pixels wide by 400 pixels high. 

Note: The following examples require that the PresentationCore (_PresentationCore.dll_) library to be referenced to the project. Use the Add Reference dialog box and select PresentationCore from the .NET tab. 

### C#
    
    
    using System.Drawing;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
     
    [CommandMethod("PositionApplicationWindow")]
    public static void PositionApplicationWindow()
    {
        // Set the position of the Application window
        System.Windows.Point ptApp = new System.Windows.Point(0, 0);
        Autodesk.AutoCAD.ApplicationServices.Application.MainWindow.DeviceIndependentLocation = ptApp;
    
        // Set the size of the Application window
        System.Windows.Size szApp = new System.Windows.Size(400, 400);
        Autodesk.AutoCAD.ApplicationServices.Application.MainWindow.DeviceIndependentSize = szApp;
    }

### VB.NET
    
    
    Imports System.Drawing
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
     
    <CommandMethod("PositionApplicationWindow")> _
    Public Sub PositionApplicationWindow()
        '' Set the position of the Application window
        Dim ptApp As System.Windows.Point = New System.Windows.Point(0, 0)
        Autodesk.AutoCAD.ApplicationServices.Core.Application.MainWindow.DeviceIndependentLocation = ptApp
    
        '' Set the size of the Application window
        Dim szApp As System.Windows.Size = New System.Windows.Size(400, 400)
        Autodesk.AutoCAD.ApplicationServices.Core.Application.MainWindow.DeviceIndependentSize = szApp
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub PositionApplicationWindow()
        '' Set the position of the Application window
        ThisDrawing.Application.WindowTop = 0
        ThisDrawing.Application.WindowLeft = 0
     
        '' Set the size of the Application window
        ThisDrawing.Application.width = 400
        ThisDrawing.Application.height = 400
    End Sub

## Minimize and maximize the Application window

Note: The following examples require that the PresentationCore (_PresentationCore.dll_) library to be referenced to the project. Use the Add Reference dialog box and select PresentationCore from the .NET tab. 

### C#
    
    
    using System.Drawing;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Windows;
     
    [CommandMethod("MinMaxApplicationWindow")]
    public static void MinMaxApplicationWindow()
    {
        //Minimize the Application window
        Application.MainWindow.WindowState = Window.State.Minimized;
    
    
        System.Windows.Forms.MessageBox.Show("Minimized", "MinMax",
                    System.Windows.Forms.MessageBoxButtons.OK,
                    System.Windows.Forms.MessageBoxIcon.None,
                    System.Windows.Forms.MessageBoxDefaultButton.Button1,
                    System.Windows.Forms.MessageBoxOptions.ServiceNotification);
    
        //Maximize the Application window
        Application.MainWindow.WindowState = Window.State.Maximized;
        System.Windows.Forms.MessageBox.Show("Maximized", "MinMax");
    }

### VB.NET
    
    
    Imports System.Drawing
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Windows
     
    <CommandMethod("MinMaxApplicationWindow")> _
    Public Sub MinMaxApplicationWindow()
        ''Minimize the Application window
        Application.MainWindow.WindowState = Window.State.Minimized
        MsgBox("Minimized", MsgBoxStyle.SystemModal, "MinMax")
    
        ''Maximize the Application window
        Application.MainWindow.WindowState = Window.State.Maximized
        MsgBox("Maximized", MsgBoxStyle.SystemModal, "MinMax")
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub MinMaxApplicationWindow()
        '' Minimize the Application window
        ThisDrawing.Application.WindowState = acMin
        MsgBox "Minimized"
     
        '' Maximize the Application window
        ThisDrawing.Application.WindowState = acMax
        MsgBox "Maximized"
    End Sub

## Find the current state of the Application window

This example queries the state of the Application window and displays the state in a message box to the user. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Windows;
     
    [CommandMethod("CurrentWindowState")]
    public static void CurrentWindowState()
    {
        System.Windows.Forms.MessageBox.Show("The application window is " +
                                                Application.MainWindow.WindowState.ToString(), 
                                                "Window State");
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Windows
     
    <CommandMethod("CurrentWindowState")> _
    Public Sub CurrentWindowState()
        System.Windows.Forms.MessageBox.Show("The application window is " + _
                                             Application.MainWindow.WindowState.ToString(), _
                                             "Window State")
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CurrentWindowState()
        Dim CurrWindowState As Integer
        Dim msg As String
        CurrWindowState = ThisDrawing.Application.WindowState
        msg = Choose(CurrWindowState, "Normal", _
                     "Minimized", "Maximized") 
        MsgBox "The application window is " + msg
    End Sub

## Make the Application window invisible and visible

The following code uses the Visible property to make the AutoCAD application window invisible and then visible again. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Windows;
     
    [CommandMethod("HideWindowState")]
    public static void HideWindowState()
    {
        //Hide the Application window
        Application.MainWindow.Visible = false;
        System.Windows.Forms.MessageBox.Show("Invisible", "Show/Hide");
    
        //Show the Application window
        Application.MainWindow.Visible = true;
        System.Windows.Forms.MessageBox.Show("Visible", "Show/Hide");
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Windows
     
    <CommandMethod("HideWindowState")> _
    Public Sub HideWindowState()
        ''Hide the Application window
        Application.MainWindow.Visible = False
        MsgBox("Invisible", MsgBoxStyle.SystemModal, "Show/Hide")
    
        ''Show the Application window
        Application.MainWindow.Visible = True
        MsgBox("Visible", MsgBoxStyle.SystemModal, "Show/Hide")
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub HideWindowState()
        '' Hide the Application window
        ThisDrawing.Application.Visible = False
        MsgBox "Invisible"
     
        '' Show the Application window
        ThisDrawing.Application.Visible = True
        MsgBox "Visible"
    End Sub
