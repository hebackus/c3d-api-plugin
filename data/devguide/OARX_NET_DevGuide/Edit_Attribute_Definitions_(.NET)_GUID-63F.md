<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use Blocks and Attributes (.NET) > Work with Attributes (.NET) > Edit Attribute Definitions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-63FE1010-F9D4-46CF-A246-CAAAFA60560B.htm -->

# Edit Attribute Definitions (.NET)

You can use the Attribute object properties and methods to edit the attribute. Some of the properties on an attribute include the following: 

FieldLength
    Specifies the field length of the attribute
Height
    Specifies the height of the attribute
HorizontalMode
    Specifies the horizontal alignment of the attribute
IsMirroredInX
    Specifies that the text of the attribute appears backwards
IsMirroredInY
    Specifies that the text of the attribute appears upside-down
Position
    Specifies the insertion point of the attribute
Prompt
    Specifies the prompt string of the attribute
Rotation
    Specifies the rotation of the attribute
Tag
    Specifies the tag string of the attribute
TextString
    Specifies the default value of the attribute
VerticalMode
    Specifies the vertical alignment of the attribute

## Redefine an attribute definition

This example creates a block and then adds an attribute to the block. The block is then inserted into the drawing. The attribute text is then updated to be displayed backward. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("RedefiningAnAttribute")]
    public void RedefiningAnAttribute()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead) as BlockTable;
    
            ObjectId blkRecId = ObjectId.Null;
    
            if (!acBlkTbl.Has("CircleBlockWithAttributes"))
            {
                using (BlockTableRecord acBlkTblRec = new BlockTableRecord())
                {
                    acBlkTblRec.Name = "CircleBlockWithAttributes";
    
                    // Set the insertion point for the block
                    acBlkTblRec.Origin = new Point3d(0, 0, 0);
    
                    // Add a circle to the block
                    using (Circle acCirc = new Circle())
                    {
                        acCirc.Center = new Point3d(0, 0, 0);
                        acCirc.Radius = 2;
    
                        acBlkTblRec.AppendEntity(acCirc);
    
                        // Add an attribute definition to the block
                        using (AttributeDefinition acAttDef = new AttributeDefinition())
                        {
                            acAttDef.Position = new Point3d(0, 0, 0);
                            acAttDef.Prompt = "Door #: ";
                            acAttDef.Tag = "Door#";
                            acAttDef.TextString = "DXX";
                            acAttDef.Height = 1;
                            acAttDef.Justify = AttachmentPoint.MiddleCenter;
                            acBlkTblRec.AppendEntity(acAttDef);
    
                            acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForWrite);
                            acBlkTbl.Add(acBlkTblRec);
                            acTrans.AddNewlyCreatedDBObject(acBlkTblRec, true);
                        }
                    }
    
                    blkRecId = acBlkTblRec.Id;
                }
            }
            else
            {
                blkRecId = acBlkTbl["CircleBlockWithAttributes"];
            }
    
            // Create and insert the new block reference
            if (blkRecId != ObjectId.Null)
            {
                BlockTableRecord acBlkTblRec;
                acBlkTblRec = acTrans.GetObject(blkRecId, OpenMode.ForRead) as BlockTableRecord;
    
                using (BlockReference acBlkRef = new BlockReference(new Point3d(2, 2, 0), blkRecId))
                {
                    BlockTableRecord acCurSpaceBlkTblRec;
                    acCurSpaceBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
    
                    acCurSpaceBlkTblRec.AppendEntity(acBlkRef);
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, true);
    
                    // Verify block table record has attribute definitions associated with it
                    if (acBlkTblRec.HasAttributeDefinitions)
                    {
                        // Add attributes from the block table record
                        foreach (ObjectId objID in acBlkTblRec)
                        {
                            DBObject dbObj = acTrans.GetObject(objID, OpenMode.ForRead) as DBObject;
    
                            if (dbObj is AttributeDefinition)
                            {
                                AttributeDefinition acAtt = dbObj as AttributeDefinition;
    
                                if (!acAtt.Constant)
                                {
                                    using (AttributeReference acAttRef = new AttributeReference())
                                    {
                                        acAttRef.SetAttributeFromBlock(acAtt, acBlkRef.BlockTransform);
                                        acAttRef.Position = acAtt.Position.TransformBy(acBlkRef.BlockTransform);
    
                                        acAttRef.TextString = acAtt.TextString;
    
                                        acBlkRef.AttributeCollection.AppendAttribute(acAttRef);
                                        acTrans.AddNewlyCreatedDBObject(acAttRef, true);
                                    }
                                }
    
                                // Change the attribute definition to be displayed as backwards
                                acTrans.GetObject(objID, OpenMode.ForWrite);
                                acAtt.IsMirroredInX = true;
                            }
                        }
                    }
                }
            }
    
            // Save the new object to the database
            acTrans.Commit();
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    <CommandMethod("RedefiningAnAttribute")> _
    Public Sub RedefiningAnAttribute()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            Dim blkRecId As ObjectId = ObjectId.Null
    
            If Not acBlkTbl.Has("CircleBlockWithAttributes") Then
                Using acBlkTblRec As New BlockTableRecord
                    acBlkTblRec.Name = "CircleBlockWithAttributes"
    
                    ' Set the insertion point for the block
                    acBlkTblRec.Origin = New Point3d(0, 0, 0)
    
                    ' Add a circle to the block
                    Using acCirc As New Circle
                        acCirc.Center = New Point3d(0, 0, 0)
                        acCirc.Radius = 2
    
                        acBlkTblRec.AppendEntity(acCirc)
    
                        ' Add an attribute definition to the block
                        Using acAttDef As New AttributeDefinition
                            acAttDef.Position = New Point3d(0, 0, 0)
                            acAttDef.Prompt = "Door #: "
                            acAttDef.Tag = "Door#"
                            acAttDef.TextString = "DXX"
                            acAttDef.Height = 1
                            acAttDef.Justify = AttachmentPoint.MiddleCenter
                            acBlkTblRec.AppendEntity(acAttDef)
    
                            acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForWrite)
                            acBlkTbl.Add(acBlkTblRec)
                            acTrans.AddNewlyCreatedDBObject(acBlkTblRec, True)
                        End Using
    
                        blkRecId = acBlkTblRec.Id
                    End Using
                End Using
            Else
                blkRecId = acBlkTbl("CircleBlockWithAttributes")
            End If
    
            ' Create and insert the new block reference
            If blkRecId <> ObjectId.Null Then
                Dim acBlkTblRec As BlockTableRecord
                acBlkTblRec = acTrans.GetObject(blkRecId, OpenMode.ForRead)
    
                Using acBlkRef As New BlockReference(New Point3d(2, 2, 0), acBlkTblRec.Id)
                    Dim acCurSpaceBlkTblRec As BlockTableRecord
                    acCurSpaceBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite)
    
                    acCurSpaceBlkTblRec.AppendEntity(acBlkRef)
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, True)
    
                    ' Verify block table record has attribute definitions associated with it
                    If acBlkTblRec.HasAttributeDefinitions Then
                        ' Add attributes from the block table record
                        For Each objID As ObjectId In acBlkTblRec
    
                            Dim dbObj As DBObject = acTrans.GetObject(objID, OpenMode.ForRead)
    
                            If TypeOf dbObj Is AttributeDefinition Then
                                Dim acAtt As AttributeDefinition = dbObj
    
                                If Not acAtt.Constant Then
                                    Using acAttRef As New AttributeReference
    
                                        acAttRef.SetAttributeFromBlock(acAtt, acBlkRef.BlockTransform)
                                        acAttRef.Position = acAtt.Position.TransformBy(acBlkRef.BlockTransform)
    
                                        acAttRef.TextString = acAtt.TextString
    
                                        acBlkRef.AttributeCollection.AppendAttribute(acAttRef)
                                        acTrans.AddNewlyCreatedDBObject(acAttRef, True)
                                    End Using
                                End If
    
                                ' Change the attribute definition to be displayed as backwards
                                acTrans.GetObject(objID, OpenMode.ForWrite)
                                acAtt.IsMirroredInX = True
                            End If
                        Next
                    End If
                End Using
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub RedefiningAnAttribute()
        ' Define the block
        Dim blockObj As AcadBlock
        Dim insertionPnt(0 To 2) As Double
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        Set blockObj = ThisDrawing.Blocks.Add(insertionPnt, "CircleBlockWithAttributes")
     
        ' Add an attribute to the block
        Dim attributeObj As AcadAttribute
        Dim height As Double
        Dim mode As Long
        Dim prompt As String
        Dim insertionPoint(0 To 2) As Double
        Dim tag As String
        Dim value As String
        height = 1
        mode = acAttributeModeVerify
        prompt = "Door #: "
        insertionPoint(0) = 0
        insertionPoint(1) = 0
        insertionPoint(2) = 0
        tag = "Door#"
        value = "DXX"
        Set attributeObj = blockObj.AddAttribute(height, mode, prompt, insertionPoint, tag, value)
    
        ' Insert the block, creating a block reference
        ' and an attribute reference
        Dim blockRefObj As AcadBlockReference
        insertionPnt(0) = 2
        insertionPnt(1) = 2
        insertionPnt(2) = 0
        Set blockRefObj = ThisDrawing.ActiveLayout.Block.InsertBlock(insertionPnt, "CircleBlockWithAttributes", 1, 1, 1, 0)
     
        ' Redefine the attribute text to display backwards.
        attributeObj.Backward = True
        attributeObj.Update
    End Sub
