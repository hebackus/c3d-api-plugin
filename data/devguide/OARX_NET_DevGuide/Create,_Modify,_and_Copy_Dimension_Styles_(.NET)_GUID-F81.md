<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Work With Dimension Styles (.NET) > Create, Modify, and Copy Dimension Styles (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F8176D55-ED39-4FAA-93F7-D6E023C1DAD1.htm -->

# Create, Modify, and Copy Dimension Styles (.NET)

A new dimension style is created by creating an instance of a DimStyleTableRecord object and then adding it to the DimStyleTable with the Add method. Before the dimension style is added to the table, set the name of the new style with the Name property. 

You can also copy an existing style or a style with overrides. Use the CopyFrom method to copy a dimension style from a source object to a dimension style. The source object can be another DimStyleTableRecord object, a Dimension, Tolerance, or Leader object, or even a Database object. If you copy the style settings from another dimension style, the current style is duplicated exactly. If you copy the style settings from a Dimension, Tolerance, or Leader object, the current settings, including any object overrides, are copied to the style. If you copy the current style of a Database object, the dimension style plus any drawing overrides are copied to the new style. 

## Copy dimension styles and overrides

This example creates three new dimension styles and copies the current settings from the current Database, a given dimension style, and a given dimension to each new dimension style respectively. By following the appropriate setup before running this example, you will find that different dimension styles have been created. 

  1. Create a new drawing and make it the active drawing. 
  2. Create a linear dimension in the new drawing. This dimension should be the only object in the drawing. 
  3. Change the color of the dimension line to yellow. 
  4. Change the DIMCLRD system variable to 5 (blue). 
  5. Run the following example: 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CopyDimStyles")]
    public static void CopyDimStyles()
    {
        // Get the current database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                            OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for read
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForRead) as BlockTableRecord;
    
            object acObj = null;
            foreach (ObjectId acObjId in acBlkTblRec)
            {
                // Get the first object in Model space
                acObj = acTrans.GetObject(acObjId,
                                            OpenMode.ForRead);
    
                break;
            }
    
            // Open the DimStyle table for read
            DimStyleTable acDimStyleTbl;
            acDimStyleTbl = acTrans.GetObject(acCurDb.DimStyleTableId,
                                                OpenMode.ForRead) as DimStyleTable;
    
            string[] strDimStyleNames = new string[3];
            strDimStyleNames[0] = "Style 1 copied from a dim";
            strDimStyleNames[1] = "Style 2 copied from Style 1";
            strDimStyleNames[2] = "Style 3 copied from the running drawing values";
    
            int nCnt = 0;
    
            // Keep a reference of the first dimension style for later
            DimStyleTableRecord acDimStyleTblRec1 = null;
    
            // Iterate the array of dimension style names
            foreach (string strDimStyleName in strDimStyleNames)
            {
                DimStyleTableRecord acDimStyleTblRec;
                DimStyleTableRecord acDimStyleTblRecCopy = null;
    
                // Check to see if the dimension style exists or not
                if (acDimStyleTbl.Has(strDimStyleName) == false)
                {
                    if (acDimStyleTbl.IsWriteEnabled == false) acTrans.GetObject(acCurDb.DimStyleTableId, OpenMode.ForWrite);
    
                    acDimStyleTblRec = new DimStyleTableRecord();
                    acDimStyleTblRec.Name = strDimStyleName;
    
                    acDimStyleTbl.Add(acDimStyleTblRec);
                    acTrans.AddNewlyCreatedDBObject(acDimStyleTblRec, true);
                }
                else
                {
                    acDimStyleTblRec = acTrans.GetObject(acDimStyleTbl[strDimStyleName],
                                                            OpenMode.ForWrite) as DimStyleTableRecord;
                }
    
                // Determine how the new dimension style is populated
                switch ((int)nCnt)
                {
                    // Assign the values of the dimension object to the new dimension style
                    case 0:
                        try
                        {
                            // Cast the object to a Dimension
                            Dimension acDim = acObj as Dimension;
    
                            // Copy the dimension style data from the dimension and
                            // set the name of the dimension style as the copied settings
                            // are unnamed.
                            acDimStyleTblRecCopy = acDim.GetDimstyleData();
                            acDimStyleTblRec1 = acDimStyleTblRec;
                        }
                        catch
                        {
                            // Object was not a dimension
                        }
    
                        break;
    
                    // Assign the values of the dimension style to the new dimension style
                    case 1:
                        acDimStyleTblRecCopy = acDimStyleTblRec1;
                        break;
                    // Assign the values of the current drawing to the dimension style
                    case 2:
                        acDimStyleTblRecCopy = acCurDb.GetDimstyleData();
                        break;
                }
    
                // Copy the dimension settings and set the name of the dimension style
                acDimStyleTblRec.CopyFrom(acDimStyleTblRecCopy);
                acDimStyleTblRec.Name = strDimStyleName;
    
                // Dispose of the copied dimension style
                acDimStyleTblRecCopy.Dispose();
    
                nCnt = nCnt + 1;
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CopyDimStyles")> _
    Public Sub CopyDimStyles()
        '' Get the current database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for read
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForRead)
    
            Dim acObj As Object = Nothing
            For Each acObjId As ObjectId In acBlkTblRec
                '' Get the first object in Model space
                acObj = acTrans.GetObject(acObjId, _
                                          OpenMode.ForRead)
    
                Exit For
            Next
    
            '' Open the DimStyle table for read
            Dim acDimStyleTbl As DimStyleTable
            acDimStyleTbl = acTrans.GetObject(acCurDb.DimStyleTableId, _
                                              OpenMode.ForRead)
    
            Dim strDimStyleNames(2) As String
            strDimStyleNames(0) = "Style 1 copied from a dim"
            strDimStyleNames(1) = "Style 2 copied from Style 1"
            strDimStyleNames(2) = "Style 3 copied from the running drawing values"
    
            Dim nCnt As Integer = 0
    
            '' Keep a reference of the first dimension style for later
            Dim acDimStyleTblRec1 As DimStyleTableRecord = Nothing
    
            '' Iterate the array of dimension style names
            For Each strDimStyleName As String In strDimStyleNames
                Dim acDimStyleTblRec As DimStyleTableRecord
                Dim acDimStyleTblRecCopy As DimStyleTableRecord = Nothing
    
                '' Check to see if the dimension style exists or not
                If acDimStyleTbl.Has(strDimStyleName) = False Then
                    If acDimStyleTbl.IsWriteEnabled = False Then acTrans.GetObject(acCurDb.DimStyleTableId, OpenMode.ForWrite)
    
                    acDimStyleTblRec = New DimStyleTableRecord()
                    acDimStyleTblRec.Name = strDimStyleName
    
                    acDimStyleTbl.Add(acDimStyleTblRec)
                    acTrans.AddNewlyCreatedDBObject(acDimStyleTblRec, True)
                Else
                    acDimStyleTblRec = acTrans.GetObject(acDimStyleTbl(strDimStyleName), _
                                                         OpenMode.ForWrite)
                End If
    
                '' Determine how the new dimension style is populated
                Select Case nCnt
                    '' Assign the values of the dimension object to the new dimension style
                    Case 0
                        Try
                            '' Cast the object to a Dimension
                            Dim acDim As RotatedDimension = acObj
    
                            '' Copy the dimension style data from the dimension and
                            '' set the name of the dimension style as the copied settings
                            '' are unnamed.
                            acDimStyleTblRecCopy = acDim.GetDimstyleData()
                            acDimStyleTblRec1 = acDimStyleTblRec
                        Catch
                            '' Object was not a dimension
                        End Try
    
                        '' Assign the values of the dimension style to the new dimension style
                    Case 1
                        acDimStyleTblRecCopy = acDimStyleTblRec1
    
                        '' Assign the values of the current drawing to the dimension style
                    Case 2
                        acDimStyleTblRecCopy = acCurDb.GetDimstyleData()
                End Select
    
                '' Copy the dimension settings and set the name of the dimension style
                acDimStyleTblRec.CopyFrom(acDimStyleTblRecCopy)
                acDimStyleTblRec.Name = strDimStyleName
    
                '' Dispose of the copied dimension style
                acDimStyleTblRecCopy.Dispose()
    
                nCnt = nCnt + 1
            Next
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CopyDimStyles()
        Dim newStyle1 As AcadDimStyle
        Dim newStyle2 As AcadDimStyle
        Dim newStyle3 As AcadDimStyle
     
        Set newStyle1 = ThisDrawing.DimStyles. _
                            Add("Style 1 copied from a dim")
        Call newStyle1.CopyFrom(ThisDrawing.ModelSpace(0))
     
        Set newStyle2 = ThisDrawing.DimStyles. _
                            Add("Style 2 copied from Style 1")
        Call newStyle2.CopyFrom(ThisDrawing.DimStyles. _
                                    Item("Style 1 copied from a dim"))
     
        Set newStyle2 = ThisDrawing.DimStyles. _
                            Add("Style 3 copied from the running drawing values")
        Call newStyle2.CopyFrom(ThisDrawing)
    End Sub

Open the Dimension Style Manager using the DIMSTYLE command. You should now have three dimension styles listed. Style 1 should have a yellow dimension line. Style 2 should be the same as Style 1. Style 3 should have a blue dimension line.
