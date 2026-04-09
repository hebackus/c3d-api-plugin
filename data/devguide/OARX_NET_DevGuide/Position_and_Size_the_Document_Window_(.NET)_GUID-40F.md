<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Position and Size the Document Window (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-40F75E13-4A5C-4F84-A5DD-38DC1FBC246B.htm -->

# Position and Size the Document Window (.NET)

Use the Document object to modify the position and size of any document window. The Document window can be minimized or maximized by using the WindowState property, and you can find the current state of the Document window by using the WindowState property. 

## Size the active Document window

This example uses the Location and Size properties to set the placement and size of Document window to 400 pixels wide by 400 pixels high. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Windows;
     
    [CommandMethod("SizeDocumentWindow")]
    public static void SizeDocumentWindow()
    {
        //Size the Document window
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        // Works around what looks to be a refresh problem with the Application window
        acDoc.Window.WindowState = Window.State.Normal;
                
        // Set the position of the Document window
        System.Windows.Point ptDoc = new System.Windows.Point(0, 0);
        acDoc.Window.DeviceIndependentLocation = ptDoc;
    
        // Set the size of the Document window
        System.Windows.Size szDoc = new System.Windows.Size(400, 400);
        acDoc.Window.DeviceIndependentSize = szDoc;
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Windows
     
    <CommandMethod("SizeDocumentWindow")> _
    Public Sub SizeDocumentWindow()
        ''Size the Document window
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        acDoc.Window.WindowState = Window.State.Normal
    
        '' Set the position of the Document window
        Dim ptDoc As System.Windows.Point = New System.Windows.Point(0, 0)
        acDoc.Window.DeviceIndependentLocation = ptdoc
    
        '' Set the size of the Document window
        Dim szDoc As System.Windows.Size = New System.Windows.Size(400, 400)
        acDoc.Window.DeviceIndependentSize = szDoc
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SizeDocumentWindow()
        ThisDrawing.Width = 400
        ThisDrawing.Height = 400
    End Sub

## Minimize and maximize the active Document window

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Windows;
     
    [CommandMethod("MinMaxDocumentWindow")]
    public static void MinMaxDocumentWindow()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        //Minimize the Document window
        acDoc.Window.WindowState = Window.State.Minimized;
        System.Windows.Forms.MessageBox.Show("Minimized" , "MinMax");
    
        //Maximize the Document window
        acDoc.Window.WindowState = Window.State.Maximized;
        System.Windows.Forms.MessageBox.Show("Maximized" , "MinMax");
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Windows
     
    <CommandMethod("MinMaxDocumentWindow")> _
    Public Sub MinMaxDocumentWindow()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        ''Minimize the Document window
        acDoc.Window.WindowState = Window.State.Minimized
        MsgBox("Minimized", MsgBoxStyle.SystemModal, "MinMax")
    
        ''Maximize the Document window
        acDoc.Window.WindowState = Window.State.Maximized
        MsgBox("Maximized", MsgBoxStyle.SystemModal, "MinMax")
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub MinMaxDocumentWindow()
        '' Minimize the Document window
        ThisDrawing.WindowState = acMin
        MsgBox "Minimized"
     
        '' Minimize the Document window
        ThisDrawing.WindowState = acMax
        MsgBox "Maximized"
    End Sub

## Find the current state of the active Document window

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Windows;
     
    [CommandMethod("CurrentDocWindowState")]
    public static void CurrentDocWindowState()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        System.Windows.Forms.MessageBox.Show("The document window is " +
        acDoc.Window.WindowState.ToString(), "Window State");
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Windows
     
    <CommandMethod("CurrentDocWindowState")> _
    Public Sub CurrentDocWindowState()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        System.Windows.Forms.MessageBox.Show("The document window is " & _
        acDoc.Window.WindowState.ToString(), "Window State")
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CurrentDocWindowState()
        Dim CurrWindowState As Integer
        Dim msg As String
        CurrWindowState = ThisDrawing.WindowState
        msg = Choose(CurrWindowState, "Normal", _
                     "Minimized", "Maximized") 
        MsgBox "The document window is " + msg
    End Sub
