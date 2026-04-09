<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use Blocks and Attributes (.NET) > Work with Attributes (.NET) > Create Attribute Definitions and Attribute References (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-2107599E-9405-4D8B-A6DD-83D603B41568.htm -->

# Create Attribute Definitions and Attribute References (.NET)

To create an attribute definition, first you must create an AttributeDefinition object and then append it to a BlockTableRecord object using the AppendEntity method. When defining an attribute definition, you should specify the height of the attribute text, the attribute modes, a prompt and tag string, the insertion point, and the default attribute value. 

The modes for the attribute definition are controlled with the following properties: 

Constant
    Gives attributes a fixed value for block insertions.
Invisible
    Specifies that attribute values are not displayed or printed when you insert the block. The ATTDISP command overrides the Invisible mode for all attributes.
IsMTextAttributeDefinition
    Specifies that the attribute value can contain multiple lines of text. When this option is selected, you can specify a boundary width for the attribute.
LockPositionInBlock
    Locks the location of the attribute within the block reference. When unlocked, the attribute can be moved relative to the rest of the block using grip editing, and multiline attributes can be resized.
Preset
    Sets the attribute to its default value when you insert a block containing a preset attribute.
Verifiable
    Prompts you to verify that the attribute value is correct when you insert the block.

The prompt string appears when a block containing the attribute is inserted and is set using the Prompt property. The default value for the attribute is set with the TextString property. If the Constant property is set to True, prompting for a new value is disabled when the block with the attribute definition is inserted. 

The tag string identifies each occurrence of the attribute and is assigned with the Tag property. You can use any characters except spaces or exclamation points. AutoCAD changes lowercase letters to uppercase. 

Once the attribute definition is defined in a block, whenever the block is inserted using the INSERT command, you can specify a different value for each attribute reference that is not defined as being constant. When a BlockReference object is created, the object does not contain any attributes that are defined in the BlockTableRecord object until they are appended to the BlockReference object using the AppendAttribute method. 

Before appending the attribute to the BlockReference object, use the SetAttributeFromBlock method to copy the properties of an AttributeDefinition object to an AttributeReference object. The HasAttributeDefinitions property can be used on a block table record to see if it contains attribute definitions. 

Attribute definitions created on model space or paper space are not considered attached to any given block. 

## Define an attribute definition

This example creates a block and then adds an attribute to the block. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("AddingAttributeToABlock")]
    public void AddingAttributeToABlock()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead) as BlockTable;
    
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
                            acAttDef.Verifiable = true;
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
    
    <CommandMethod("AddingAttributeToABlock")> _
    Public Sub AddingAttributeToABlock()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
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
                            acAttDef.Verifiable = True
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
                    End Using
                End Using
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AddingAttributeToABlock ()
        ' Define the block
        Dim blockObj As AcadBlock
        Dim insertionPnt(0 To 2) As Double
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        Set blockObj = ThisDrawing.Blocks.Add(insertionPnt, "CircleBlockWithAttributes")
    
        ' Add a circle to the block
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 0
        center(1) = 0
        center(2) = 0
        radius = 2
        Set circleObj = blockObj.AddCircle(center, radius)
     
        ' Add an attribute to the block
        Dim attributeObj As AcadAttribute
        Dim height As Double
        Dim mode As Long
        Dim prompt As String
        Dim insertionPoint(0 To 2) As Double
        Dim tag As String
        Dim value As String
        insertionPoint(0) = 0
        insertionPoint(1) = 0
        insertionPoint(2) = 0
        height = 1
        prompt = "Door #: "
        tag = "Door#"
        value = "DXX"
        
        Set attributeObj = blockObj.AddAttribute(height, mode, prompt, insertionPoint, tag, value)
        attributeObj.Alignment = acAlignmentMiddleCenter
    End Sub

## Insert a block with attributes

This example creates a block with attributes, and then inserts the block in the current space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("InsertingBlockWithAnAttribute")]
    public void InsertingBlockWithAnAttribute()
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
    
            // Insert the block into the current space
            if (blkRecId != ObjectId.Null)
            {
                BlockTableRecord acBlkTblRec;
                acBlkTblRec = acTrans.GetObject(blkRecId, OpenMode.ForRead) as BlockTableRecord;
    
                // Create and insert the new block reference
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
    
    <CommandMethod("InsertingBlockWithAnAttribute")> _
    Public Sub InsertingBlockWithAnAttribute()
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
    
    
    Sub InsertingBlockWithAnAttribute ()
        ' Define the block
        Dim blockObj As AcadBlock
        Dim insertionPnt(0 To 2) As Double
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        Set blockObj = ThisDrawing.Blocks.Add(insertionPnt, "CircleBlockWithAttributes")
    
        ' Add a circle to the block
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 0
        center(1) = 0
        center(2) = 0
        radius = 2
        Set circleObj = blockObj.AddCircle(center, radius)
     
        ' Add an attribute to the block
        Dim attributeObj As AcadAttribute
        Dim height As Double
        Dim mode As Long
        Dim prompt As String
        Dim insertionPoint(0 To 2) As Double
        Dim tag As String
        Dim value As String
        insertionPoint(0) = 0
        insertionPoint(1) = 0
        insertionPoint(2) = 0
        height = 1
        prompt = "Door #: "
        tag = "Door#"
        value = "DXX"
        
        Set attributeObj = blockObj.AddAttribute(height, mode, prompt, insertionPoint, tag, value)
        attributeObj.Alignment = acAlignmentMiddleCenter
        
        ' Insert the block, creating a block reference
        ' and an attribute reference
        Dim blockRefObj As AcadBlockReference
        insertionPnt(0) = 2
        insertionPnt(1) = 2
        insertionPnt(2) = 0
        Set blockRefObj = ThisDrawing.ActiveLayout.Block.InsertBlock(insertionPnt, "CircleBlockWithAttributes", 1, 1, 1, 0)
    End Sub
