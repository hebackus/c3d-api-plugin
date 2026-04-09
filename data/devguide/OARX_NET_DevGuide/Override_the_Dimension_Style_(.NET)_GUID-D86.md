<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Work With Dimension Styles (.NET) > Override the Dimension Style (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D86FAE33-CF6E-4BAD-AB77-DA5A5C6E8E57.htm -->

# Override the Dimension Style (.NET)

Each dimension has the capability of overriding the settings assigned to it by a dimension style. The following properties are available for most dimension objects: 

Dimatfit
    

Specifies the display of dimension lines inside extension lines only, and forces dimension text and arrowheads inside or outside extension lines. 

Dimaltrnd
    

Specifies the rounding of alternate units. 

Dimasz
    

Specifies the size of dimension line arrowheads, leader line arrowheads, and hook lines. 

Dimaunit
    

Specifies the unit format for angular dimensions. 

Dimblk1, Dimblk2
    

Specifies the blocks to use for arrowheads of the dimension line. 

Dimcen
    

Specifies the type and size of center mark for radial and diametric dimensions. 

Dimclrd
    

Specifies the color of the dimension line for a dimension, leader, or tolerance object. 

Dimclre
    

Specifies the color for dimension extension lines. 

Dimclrt
    

Specifies the color of the text for dimension and tolerance objects. 

Dimdec
    

Specifies the number of decimal places displayed for the primary units of a dimension or tolerance. 

Dimdsep
    

Specifies the character to be used as the decimal separator in decimal dimension and tolerance values. 

Dimexe
    

Specifies the distance the extension line extends beyond the dimension line. 

Dimexo
    

Specifies the distance the extension lines are offset from the origin points. 

Dimfrac
    

Specifies the format of fractional values in dimensions and tolerances. 

Dimgap
    

Specifies the distance between the dimension text and the dimension line when you break the dimension line to accommodate dimension text. 

Dimlfac
    

Specifies a global scale factor for linear dimension measurements. 

Dimltex1, Dimltex2
    

Specifies the linetypes for the extension lines. 

Dimlwd
    

Specifies the lineweight for the dimension line. 

Dimlwe
    

Specifies the lineweight for the extension lines. 

Dimjust
    

Specifies the horizontal justification for dimension text. 

Dimrnd
    

Specifies the distance rounding for dimension measurements. 

Dimsd1, Dimsd2
    

Specifies the suppression of the dimension lines. 

Dimse1, Dimse2
    

Specifies the suppression of extension lines. 

Dimtad
    

Specifies the vertical position of text in relation to the dimension line. 

Dimtdec
    

Specifies the precision of tolerance values in primary dimensions. 

Dimtfac
    

Specifies a scale factor for the text height of tolerance values relative to the dimension text height. 

Dimlunit
    

Specifies the unit format for all dimensions except angular. 

Dimtih
    

Specifies if the dimension text is to be drawn inside the extension lines. 

Dimtm
    

Specifies the minimum tolerance limit for dimension text. 

Dimtmove
    

Specifies how dimension text is drawn when text is moved. 

Dimtofl
    

Specifies if a dimension line is drawn between the extension lines even when the text is placed outside the extension lines. 

Dimtoh
    

Specifies the position of dimension text outside the extension lines for all dimension types except ordinate. 

Dimtol
    

Specifies if tolerances are displayed with the dimension text. 

Dimtolj
    

Specifies the vertical justification of tolerance values relative to the nominal dimension text. 

Dimtp
    

Specifies the maximum tolerance limit for dimension text. 

Dimtxt
    

Specifies the height for the dimension or tolerance text. 

Dimzin
    

Specifies the suppression of leading and trailing zeros, and zero foot and inch measurements in dimension values. 

Prefix
    

Specifies the dimension value prefix. 

Suffix
    

Specifies the dimension value suffix. 

TextPrecision
    

Specifies the precision of angular dimension text. 

TextPosition
    

Specifies the dimension text position. 

TextRotation
    

Specifies the rotation angle of the dimension text. 

## Enter a user-defined suffix for an aligned dimension

This example creates an aligned dimension in model space and uses the Suffix property to allow the user to change the text suffix for the dimension. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddDimensionTextSuffix")]
    public static void AddDimensionTextSuffix()
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
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create the aligned dimension
            using (AlignedDimension acAliDim = new AlignedDimension())
            {
                acAliDim.XLine1Point = new Point3d(0, 5, 0);
                acAliDim.XLine2Point = new Point3d(5, 5, 0);
                acAliDim.DimLinePoint = new Point3d(5, 7, 0);
                acAliDim.DimensionStyle = acCurDb.Dimstyle;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acAliDim);
                acTrans.AddNewlyCreatedDBObject(acAliDim, true);
    
                // Append a suffix to the dimension text
                PromptStringOptions pStrOpts = new PromptStringOptions("");
    
                pStrOpts.Message = "\nEnter a new text suffix for the dimension: ";
                pStrOpts.AllowSpaces = true;
                PromptResult pStrRes = acDoc.Editor.GetString(pStrOpts);
    
                if (pStrRes.Status == PromptStatus.OK)
                {
                    acAliDim.Suffix = pStrRes.StringResult;
                }
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("AddDimensionTextSuffix")> _
    Public Sub AddDimensionTextSuffix()
        '' Get the current database
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
    
            '' Create the aligned dimension
            Using acAliDim As AlignedDimension = New AlignedDimension()
                acAliDim.XLine1Point = New Point3d(0, 5, 0)
                acAliDim.XLine2Point = New Point3d(5, 5, 0)
                acAliDim.DimLinePoint = New Point3d(5, 7, 0)
                acAliDim.DimensionStyle = acCurDb.Dimstyle
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acAliDim)
                acTrans.AddNewlyCreatedDBObject(acAliDim, True)
    
                '' Append a suffix to the dimension text
                Dim pStrOpts As PromptStringOptions = New PromptStringOptions("")
    
                pStrOpts.Message = vbLf & "Enter a new text suffix for the dimension: "
                pStrOpts.AllowSpaces = True
                Dim pStrRes As PromptResult = acDoc.Editor.GetString(pStrOpts)
    
                If pStrRes.Status = PromptStatus.OK Then
                    acAliDim.Suffix = pStrRes.StringResult
                End If
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AddDimensionTextSuffix()
        Dim dimObj As AcadDimAligned
        Dim point1(0 To 2) As Double
        Dim point2(0 To 2) As Double
        Dim location(0 To 2) As Double
        Dim suffix As String
     
        ' Define the dimension
        point1(0) = 0: point1(1) = 5: point1(2) = 0
        point2(0) = 5: point2(1) = 5: point2(2) = 0
        location(0) = 5: location(1) = 7: location(2) = 0
     
        ' Create an aligned dimension object in model space
        Set dimObj = ThisDrawing.ModelSpace. _
                         AddDimAligned(point1, point2, location)
     
        ThisDrawing.Application.ZoomAll
        ' Allow the user to change the text suffix for the dimension
        suffix = ThisDrawing.Utility. _
                     GetString(True, vbLf & "Enter a new text " & _
                                            "suffix for the dimension: ")
     
        ' Apply the change to the dimension
        dimObj.TextSuffix = suffix
        ThisDrawing.Regen acAllViewports
    End Sub
