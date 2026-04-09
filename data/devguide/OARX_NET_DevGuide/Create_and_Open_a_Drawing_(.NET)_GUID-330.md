<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Create, Open, Save, and Close Drawings (.NET) > Create and Open a Drawing (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-330A8DCB-626F-4271-8B89-9773A7631D87.htm -->

# Create and Open a Drawing (.NET)

To create a new drawing or open an existing drawing, use the methods of the DocumentCollectionExtension object. The Add method creates a new drawing file based on a drawing template and adds that drawing to the DocumentCollectionExtension. The Open method opens an existing drawing file. 

## Create a new drawing

This example uses the Add method to create a new drawing based on the _acad.dwt_ drawing template file. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("NewDrawing", CommandFlags.Session)]
    public static void NewDrawing()
    {
        // Specify the template to use, if the template is not found
        // the default settings are used.
        string strTemplatePath = "acad.dwt";
    
        DocumentCollection acDocMgr = Application.DocumentManager;
        Document acDoc = acDocMgr.Add(strTemplatePath);
    
        acDocMgr.MdiActiveDocument = acDoc;
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("NewDrawing", CommandFlags.Session)> _
    Public Sub NewDrawing()
        '' Specify the template to use, if the template is not found
        '' the default settings are used.
        Dim strTemplatePath As String = "acad.dwt"
    
        Dim acDocMgr As DocumentCollection = Application.DocumentManager
        Dim acDoc As Document = DocumentCollectionExtension.Add(acDocMgr, strTemplatePath)
    
        acDocMgr.MdiActiveDocument = acDoc
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub NewDrawing()
        Dim strTemplatePath As String
        strTemplatePath = "acad.dwt"
     
        Dim docObj As AcadDocument
        Set docObj = ThisDrawing.Application.Documents.Add(strTemplatePath)
    End Sub

## Open an existing drawing

This example uses the Open method to open an existing drawing. Before opening the drawing, the code checks for the existence of the file before trying to open it. 

### C#
    
    
    using System.IO;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("OpenDrawing", CommandFlags.Session)]
    public static void OpenDrawing()
    {
        string strFileName = "C:\\campus.dwg";
        DocumentCollection acDocMgr = Application.DocumentManager;
    
        if (File.Exists(strFileName))
        {
            acDocMgr.Open(strFileName, false);
        }
        else
        {
            acDocMgr.MdiActiveDocument.Editor.WriteMessage("File " + strFileName +
                                                            " does not exist.");
        }
    }

### VB.NET
    
    
    Imports System.IO
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("OpenDrawing", CommandFlags.Session)> _
    Public Sub OpenDrawing()
        Dim strFileName As String = "C:\campus.dwg"
    
        Dim acDocMgr As DocumentCollection = Application.DocumentManager
    
        If (File.Exists(strFileName)) Then
            DocumentCollectionExtension.Open(acDocMgr, strFileName, False)
        Else
            acDocMgr.MdiActiveDocument.Editor.WriteMessage("File " & strFileName & _
                                                           " does not exist.")
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub OpenDrawing()
        Dim dwgName As String
        dwgName = "c:\campus.dwg"
        If Dir(dwgName) <> "" Then
            ThisDrawing.Application.Documents.Open dwgName
        Else
            MsgBox "File " & dwgName & " does not exist."
        End If
    End Sub
