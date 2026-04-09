<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) > Sort Layers and Linetypes (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8C2502C9-ED82-4956-BA45-6A87ED4D676B.htm -->

# Sort Layers and Linetypes (.NET)

You can iterate through the Layers and Linetypes tables to find all the layers and linetypes in a drawing. 

## Iterate through the Layers table

The following code iterates through the Layers table to gather the names of all the layers in the drawing. The names are then displayed in a message box. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("DisplayLayerNames")]
    public static void DisplayLayerNames()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Layer table for read
            LayerTable acLyrTbl;
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                         OpenMode.ForRead) as LayerTable;
    
            string sLayerNames = "";
    
            foreach (ObjectId acObjId in acLyrTbl)
            {
                LayerTableRecord acLyrTblRec;
                acLyrTblRec = acTrans.GetObject(acObjId,
                                                OpenMode.ForRead) as LayerTableRecord;
    
                sLayerNames = sLayerNames + "\n" + acLyrTblRec.Name;
            }
    
            Application.ShowAlertDialog("The layers in this drawing are: " +
                                        sLayerNames);
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("DisplayLayerNames")> _
    Public Sub DisplayLayerNames()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Layer table for read
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                         OpenMode.ForRead)
    
            Dim sLayerNames As String = ""
    
            For Each acObjId As ObjectId In acLyrTbl
                Dim acLyrTblRec As LayerTableRecord
                acLyrTblRec = acTrans.GetObject(acObjId, _
                                                OpenMode.ForRead)
    
                sLayerNames = sLayerNames & vbLf & acLyrTblRec.Name
            Next
    
            Application.ShowAlertDialog("The layers in this drawing are: " & _
                                        sLayerNames)
    
            '' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub DisplayLayerNames()
        Dim layerNames As String
        Dim entry As AcadLayer
        layerNames = ""
     
        For Each entry In ThisDrawing.Layers
            layerNames = layerNames + entry.Name + vbCrLf
        Next
     
        MsgBox "The layers in this drawing are: " + _
               vbCrLf + layerNames
    End Sub
