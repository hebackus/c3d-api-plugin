<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Dimensions (.NET) > Create Linear Dimensions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-AB746B0F-3C24-4206-9BED-5881DDED606C.htm -->

# Create Linear Dimensions (.NET)

Linear dimensions can be aligned or rotated. Aligned dimensions have the dimension line parallel to the line along which the extension line origins lie. Rotated dimensions have the dimension line placed at an angle to the extension line origins. 

You create linear dimensions by creating instances of the AlignedDimension and RotatedDimension objects. After you create an instance of a linear dimensions, you can modify the text, the angle of the text, or the angle of the dimension line. The following illustrations show how the type of linear dimension and the placement of the extension line origins affect the angle of the dimension line and text. 

When you create an instance of an AlignedDimension object, you have the option to specify the extension line origins, the location of the dimension line, dimension text, and the dimension style to apply. If you do not pass any parameters into the AlignedDimension object constructor, the object is assigned a set of default property values. 

The RotatedDimension object constructor offers the same options as the AlignedDimension object constructor, with one exception. The RotatedDimension object constructor takes an additional parameter that specifies the angle at which the dimension line is rotated. 

## Dimension joglines

Joglines on linear dimensions are not added through a set of properties, but extended data (Xdata). The application name responsible for dimension joglines is ACAD_DSTYLE_DIMJAG_POSITION. The following is an example of the Xdata structure that needs to be appended to a linear dimension. 

### C#
    
    
    // Open the Registered Application table for read
    RegAppTable acRegAppTbl;
    acRegAppTbl = <transaction>.GetObject(<current_database>.RegAppTableId,
                                          OpenMode.ForRead) as RegAppTable;
     
    // Check to see if the app "ACAD_DSTYLE_DIMJAG_POSITION" is
    // registered and if not add it to the RegApp table
    if (acRegAppTbl.Has("ACAD_DSTYLE_DIMJAG_POSITION") == false)
    {
        using (RegAppTableRecord acRegAppTblRec = new RegAppTableRecord())
        {
            acRegAppTblRec.Name = "ACAD_DSTYLE_DIMJAG_POSITION";
     
            <transaction>.GetObject(<current_database>.RegAppTableId, OpenMode.ForWrite);
     
            acRegAppTbl.Add(acRegAppTblRec);
            <transaction>.AddNewlyCreatedDBObject(acRegAppTblRec, true);
        }
    }
     
    // Create a result buffer to define the Xdata
    ResultBuffer acResBuf = new ResultBuffer();
    acResBuf.Add(new TypedValue((int)DxfCode.ExtendedDataRegAppName,
                                             "ACAD_DSTYLE_DIMJAG_POSITION"));
    acResBuf.Add(new TypedValue((int)DxfCode.ExtendedDataInteger16, 387));
    acResBuf.Add(new TypedValue((int)DxfCode.ExtendedDataInteger16, 3));
    acResBuf.Add(new TypedValue((int)DxfCode.ExtendedDataInteger16, 389));
    acResBuf.Add(new TypedValue((int)DxfCode.ExtendedDataXCoordinate,
                                             new Point3d(-1.26985, 3.91514, 0)));
     
    // Attach the Xdata to the dimension
    <dimension_object>.XData = acResBuf;

### VB.NET
    
    
    '' Open the Registered Application table for read
    Dim acRegAppTbl As RegAppTable
    acRegAppTbl = <transaction>.GetObject(<current_database>.RegAppTableId, _
                                          OpenMode.ForRead)
     
    '' Check to see if the app "ACAD_DSTYLE_DIMJAG_POSITION" is
    '' registered and if not add it to the RegApp table
    If acRegAppTbl.Has("ACAD_DSTYLE_DIMJAG_POSITION") = False Then
        Using acRegAppTblRec As RegAppTableRecord = New RegAppTableRecord()
     
            acRegAppTblRec.Name = "ACAD_DSTYLE_DIMJAG_POSITION"
     
            <transaction>.GetObject(<current_database>.RegAppTableId, OpenMode.ForWrite)
     
            acRegAppTbl.Add(acRegAppTblRec)
            <transaction>.AddNewlyCreatedDBObject(acRegAppTblRec, True)
        End Using
    End If
     
    '' Create a result buffer to define the Xdata
    Dim acResBuf As ResultBuffer = New ResultBuffer()
    acResBuf.Add(New TypedValue(DxfCode.ExtendedDataRegAppName, _
                                        "ACAD_DSTYLE_DIMJAG_POSITION"))
    acResBuf.Add(New TypedValue(DxfCode.ExtendedDataInteger16, 387))
    acResBuf.Add(New TypedValue(DxfCode.ExtendedDataInteger16, 3))
    acResBuf.Add(New TypedValue(DxfCode.ExtendedDataInteger16, 389))
    acResBuf.Add(New TypedValue(DxfCode.ExtendedDataXCoordinate, _
                                        New Point3d(-1.26985, 3.91514, 0)))
     
    '' Attach the Xdata to the dimension
    <dimension_object>.XData = acResBuf

### VBA/ActiveX Code Reference
    
    
    Dim DataType(0 To 4) As Integer
    Dim Data(0 To 4) As Variant
    Dim jogPoint(0 To 2) As Double
     
    DataType(0) = 1001: Data(0) = "ACAD_DSTYLE_DIMJAG_POSITION"
    DataType(1) = 1070: Data(1) = 387
    DataType(2) = 1070: Data(2) = 3
    DataType(3) = 1070: Data(3) = 389
     
    jogPoint(0) = -1.26985: jogPoint(1) = 3.91514: jogPoint(2) = 0#
    DataType(4) = 1010: Data(4) = jogPoint
     
    ' Attach the xdata to the dimension
    <dimension_object>.SetXData DataType, Data

## Create a rotated linear dimension

This example creates a rotated dimension in Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateRotatedDimension")]
    public static void CreateRotatedDimension()
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
    
            // Create the rotated dimension
            using (RotatedDimension acRotDim = new RotatedDimension())
            {
                acRotDim.XLine1Point = new Point3d(0, 0, 0);
                acRotDim.XLine2Point = new Point3d(6, 3, 0);
                acRotDim.Rotation = 0.707;
                acRotDim.DimLinePoint = new Point3d(0, 5, 0);
                acRotDim.DimensionStyle = acCurDb.Dimstyle;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acRotDim);
                acTrans.AddNewlyCreatedDBObject(acRotDim, true);
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
     
    <CommandMethod("CreateRotatedDimension")> _
    Public Sub CreateRotatedDimension()
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
    
            '' Create the rotated dimension
            Using acRotDim As RotatedDimension = New RotatedDimension()
                acRotDim.XLine1Point = New Point3d(0, 0, 0)
                acRotDim.XLine2Point = New Point3d(6, 3, 0)
                acRotDim.Rotation = 0.707
                acRotDim.DimLinePoint = New Point3d(0, 5, 0)
                acRotDim.DimensionStyle = acCurDb.Dimstyle
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acRotDim)
                acTrans.AddNewlyCreatedDBObject(acRotDim, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateRotatedDimension()
        Dim dimObj As AcadDimRotated
        Dim rotationAngle As Double
        Dim startExtPoint(0 To 2) As Double
        Dim endExtPoint(0 To 2) As Double
        Dim dimLinePoint(0 To 2) As Double
     
        ' Define the dimension
        rotationAngle = 0.707
        startExtPoint(0) = 0: startExtPoint(1) = 0: startExtPoint(2) = 0
        endExtPoint(0) = 6: endExtPoint(1) = 3: endExtPoint(2) = 0
        dimLinePoint(0) = 0: dimLinePoint(1) = 5: dimLinePoint(2) = 0
     
        ' Create the rotated dimension in Model space
        Set dimObj = ThisDrawing.ModelSpace. _
                                     AddDimRotated(startExtPoint, endExtPoint, _
                                                   dimLinePoint, rotationAngle)
        ZoomAll
    End Sub
