<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Single-Line Text (.NET) > Format Single-Line Text (.NET) > Align Single-Line Text (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8B9FD3E9-C3B1-4F2D-B52C-215299183D76.htm -->

# Align Single-Line Text (.NET)

You can justify single-line text horizontally and vertically. Left alignment is the default. To set the horizontal and vertical alignment options, use the HorizontalMode and VerticalMode properties. 

Normally when a text object is closed, the position and alignment points of the text object are adjusted according to its justification and text style. However, the alignment of an in memory text object will not automatically be updated. Call the AdjustAlignment method to update the alignment of the text object based on its current property values. 

## Realign text

The following example creates a single-line text (DBText) object and a point (DBPoint) object. The point object is set to the text alignment point, and is changed to a red crosshair so that it is visible. The text alignment is changed and a message box is displayed so that the macro execution is halted. This allows you to see the impact of changing the text alignment. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("TextAlignment")]
    public static void TextAlignment()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            string[] textString = new string[3];
            textString[0] = "Left";
            textString[1] = "Center";
            textString[2] = "Right";
    
            int[] textAlign = new int[3];
            textAlign[0] = (int)TextHorizontalMode.TextLeft;
            textAlign[1] = (int)TextHorizontalMode.TextCenter;
            textAlign[2] = (int)TextHorizontalMode.TextRight;
    
            Point3d acPtIns = new Point3d(3, 3, 0);
            Point3d acPtAlign = new Point3d(3, 3, 0);
    
            int nCnt = 0;
    
            foreach (string strVal in textString)
            {
                // Create a single-line text object
                using (DBText acText = new DBText())
                {
                    acText.Position = acPtIns;
                    acText.Height = 0.5;
                    acText.TextString = strVal;
    
                    // Set the alignment for the text
                    acText.HorizontalMode = (TextHorizontalMode)textAlign[nCnt];
    
                    if (acText.HorizontalMode != TextHorizontalMode.TextLeft)
                    {
                        acText.AlignmentPoint = acPtAlign;
                    }
    
                    acBlkTblRec.AppendEntity(acText);
                    acTrans.AddNewlyCreatedDBObject(acText, true);
                }
    
                // Create a point over the alignment point of the text
                using (DBPoint acPoint = new DBPoint(acPtAlign))
                {
                    acPoint.ColorIndex = 1;
    
                    acBlkTblRec.AppendEntity(acPoint);
                    acTrans.AddNewlyCreatedDBObject(acPoint, true);
    
                    // Adjust the insertion and alignment points
                    acPtIns = new Point3d(acPtIns.X, acPtIns.Y + 3, 0);
                    acPtAlign = acPtIns;
                }
    
                nCnt = nCnt + 1;
            }
    
            // Set the point style to crosshair
            Application.SetSystemVariable("PDMODE", 2);
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("TextAlignment")> _
    Public Sub TextAlignment()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            Dim textString(0 To 2) As String
            textString(0) = "Left"
            textString(1) = "Center"
            textString(2) = "Right"
    
            Dim textAlign(0 To 2) As Integer
            textAlign(0) = TextHorizontalMode.TextLeft
            textAlign(1) = TextHorizontalMode.TextCenter
            textAlign(2) = TextHorizontalMode.TextRight
    
            Dim acPtIns As Point3d = New Point3d(3, 3, 0)
            Dim acPtAlign As Point3d = New Point3d(3, 3, 0)
    
            Dim nCnt As Integer = 0
    
            For Each strVal As String In textString
                '' Create a single-line text object
                Using acText As DBText = New DBText()
                    acText.Position = acPtIns
                    acText.Height = 0.5
                    acText.TextString = strVal
    
                    '' Set the alignment for the text
                    acText.HorizontalMode = textAlign(nCnt)
    
                    If acText.HorizontalMode <> TextHorizontalMode.TextLeft Then
                        acText.AlignmentPoint = acPtAlign
                    End If
    
                    acBlkTblRec.AppendEntity(acText)
                    acTrans.AddNewlyCreatedDBObject(acText, True)
                End Using
    
                '' Create a point over the alignment point of the text
                Using acPoint As DBPoint = New DBPoint(acPtAlign)
                    acPoint.ColorIndex = 1
    
                    acBlkTblRec.AppendEntity(acPoint)
                    acTrans.AddNewlyCreatedDBObject(acPoint, True)
    
                    '' Adjust the insertion and alignment points
                    acPtIns = New Point3d(acPtIns.X, acPtIns.Y + 3, 0)
                    acPtAlign = acPtIns
                End Using
    
                nCnt = nCnt + 1
            Next
    
            '' Set the point style to crosshair
            Application.SetSystemVariable("PDMODE", 2)
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub TextAlignment()
        ' Set the point style to crosshair
        ThisDrawing.SetVariable "PDMODE", 2
     
        Dim textObj As AcadText
        Dim pointObj As AcadPoint
     
        ' Define the text strings and insertion point for the text objects
        Dim textString(0 To 2) As String
        textString(0) = "Left"
        textString(1) = "Center"
        textString(2) = "Right"
     
        Dim textAlign(0 To 2) As Integer
        textAlign(0) = acAlignmentLeft
        textAlign(1) = acAlignmentCenter
        textAlign(2) = acAlignmentRight
     
        Dim insertionPoint(0 To 2) As Double
        insertionPoint(0) = 3: insertionPoint(1) = 0: insertionPoint(2) = 0
     
        Dim alignmentPoint(0 To 2) As Double
        alignmentPoint(0) = 3: alignmentPoint(1) = 0: alignmentPoint(2) = 0
     
        Dim nCnt As Integer
        For Each strVal In textString
            ' Create the Text object in model space
            Set textObj = ThisDrawing.ModelSpace. _
                            AddText(strVal, insertionPoint, 0.5)
     
            ' Set the alignment for the text
            textObj.Alignment = textAlign(nCnt)
     
            On Error Resume Next
            textObj.TextAlignmentPoint = alignmentPoint
     
            ' Create a point over the alignment point of the text
            Set pointObj = ThisDrawing.ModelSpace.AddPoint(alignmentPoint)
            pointObj.color = acRed
     
            ' Adjust the insertion and alignment points
            insertionPoint(1) = insertionPoint(1) + 3
            alignmentPoint(1) = insertionPoint(1)
     
            nCnt = nCnt + 1
        Next
    End Sub
