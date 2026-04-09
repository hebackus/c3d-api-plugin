<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Save and Restore Layer States (.NET) > Use the LayerStateManager to Manage Layer States (.NET) > Rename Layer States (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-EC776934-5880-4BCA-A149-7871E1A8CA68.htm -->

# Rename Layer States (.NET)

The RenameLayerState method renames a saved layer state from one name to another in a drawing. The following code renames the ColorLinetype layer settings to OldColorLinetype. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("RenameLayerState")]
    public static void RenameLayerState()
    {
        // Get the current document
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
        LayerStateManager acLyrStMan;
        acLyrStMan = acDoc.Database.LayerStateManager;
     
        string sLyrStName = "ColorLinetype";
        string sLyrStNewName = "OldColorLinetype";
     
        if (acLyrStMan.HasLayerState(sLyrStName) == true &&
            acLyrStMan.HasLayerState(sLyrStNewName) == false)
        {
            acLyrStMan.RenameLayerState(sLyrStName, sLyrStNewName);
        }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("RenameLayerState")> _
    Public Sub RenameLayerState()
        '' Get the current document
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
        Dim acLyrStMan As LayerStateManager
        acLyrStMan = acDoc.Database.LayerStateManager
     
        Dim sLyrStName As String = "ColorLinetype"
        Dim sLyrStNewName As String = "OldColorLinetype"
     
        If acLyrStMan.HasLayerState(sLyrStName) = True And _
           acLyrStMan.HasLayerState(sLyrStNewName) = False Then
            acLyrStMan.RenameLayerState(sLyrStName, sLyrStNewName)
        End If
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub RenameLayerState()
        Dim oLSM As AcadLayerStateManager
        Set oLSM = ThisDrawing.Application. _
                       GetInterfaceObject("AutoCAD.AcadLayerStateManager.25")
     
        oLSM.SetDatabase ThisDrawing.Database
        oLSM.Rename "ColorLinetype", "OldColorLinetype"
    End Sub
