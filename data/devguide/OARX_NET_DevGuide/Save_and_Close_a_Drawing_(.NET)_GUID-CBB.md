<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Create, Open, Save, and Close Drawings (.NET) > Save and Close a Drawing (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CBB74093-BB22-49CC-B54A-D33D7E92694C.htm -->

# Save and Close a Drawing (.NET)

Use the SaveAs method of the Database object to save the contents of a Database object. When using the SaveAs method, you can specify if the database should be renamed and if a backup of the drawing on disk should be renamed to a backup file by providing True for the bBakAndRename parameter. You can determine if a database is using a default name of Drawing1, Drawing2, etc by checking the value of the DWGTITLED system variable. If DWGTITLED is 0, the drawing has not been renamed. 

Occasionally, you will want to check if the active drawing has any unsaved changes. It is a good idea to do this before you quit the AutoCAD session or start a new drawing. To check to see if a drawing file has been changed, you need to check the value of the DBMOD system variable. 

## Close a Drawing

The CloseAndDiscard or CloseAndSave methods of the Document object are used to close an open drawing and discard or save any changes made. You can use the CloseAll method of the DocumentCollectionExtension to close all open drawings in the AutoCAD. 

## Save the active drawing

This example saves the active drawing to "_c:\MyDrawing.dwg_ " if it is currently not saved or under its current name. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("SaveActiveDrawing")]
    public static void SaveActiveDrawing()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        string strDWGName = acDoc.Name;
     
        object obj = Application.GetSystemVariable("DWGTITLED");
     
        // Check to see if the drawing has been named
        if (System.Convert.ToInt16(obj) == 0)
        {
            // If the drawing is using a default name (Drawing1, Drawing2, etc)
            // then provide a new name
            strDWGName = "c:\\MyDrawing.dwg";
        }
     
        // Save the active drawing
        acDoc.Database.SaveAs(strDWGName, true, DwgVersion.Current,
                              acDoc.Database.SecurityParameters);
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("SaveActiveDrawing")> _
    Public Sub SaveActiveDrawing()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim strDWGName As String = acDoc.Name
     
        Dim obj As Object = Application.GetSystemVariable("DWGTITLED")
     
        '' Check to see if the drawing has been named
        If System.Convert.ToInt16(obj) = 0 Then
            '' If the drawing is using a default name (Drawing1, Drawing2, etc)
            '' then provide a new name
            strDWGName = "c:\MyDrawing.dwg"
        End If
     
        '' Save the active drawing
        acDoc.Database.SaveAs(strDWGName, True, DwgVersion.Current, _
                              acDoc.Database.SecurityParameters)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SaveActiveDrawing()
        ' Save the active drawing under a new name
        ThisDrawing.SaveAs "MyDrawing.dwg"
    End Sub

## Determine if a drawing has unsaved changes

This example checks to see if there are unsaved changes and verifies with the user that it is OK to save the drawing (if it is not OK, skip to the end). If OK, use the SaveAs method to save the current drawing, as shown here: 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("DrawingSaved")]
    public static void DrawingSaved()
    {
        object obj = Application.GetSystemVariable("DBMOD");
     
        // Check the value of DBMOD, if 0 then the drawing has no unsaved changes
        if (System.Convert.ToInt16(obj) != 0)
        {
            if (System.Windows.Forms.MessageBox.Show("Do you wish to save this drawing?",
                                      "Save Drawing",
                                      System.Windows.Forms.MessageBoxButtons.YesNo,
                                      System.Windows.Forms.MessageBoxIcon.Question)
                                      == System.Windows.Forms.DialogResult.Yes)
            {
                Document acDoc = Application.DocumentManager.MdiActiveDocument;
                acDoc.Database.SaveAs(acDoc.Name, true, DwgVersion.Current,
                                      acDoc.Database.SecurityParameters);
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("DrawingSaved")> _
    Public Sub DrawingSaved()
        Dim obj As Object = Application.GetSystemVariable("DBMOD")
     
        '' Check the value of DBMOD, if 0 then the drawing has not been changed
        If Not (System.Convert.ToInt16(obj) = 0) Then
            If MsgBox("Do you wish to save this drawing?", _
                      MsgBoxStyle.YesNo, _
                      "Save Drawing") = MsgBoxResult.Yes Then
                Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
                acDoc.Database.SaveAs(acDoc.Name, True, DwgVersion.Current, _
                                      acDoc.Database.SecurityParameters)
            End If
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub DrawingSaved()
        If Not (ThisDrawing.Saved) Then
            If MsgBox("Do you wish to save this drawing?", _
                      vbYesNo) = vbYes Then
                ThisDrawing.Save
            End If
        End If
    End Sub
