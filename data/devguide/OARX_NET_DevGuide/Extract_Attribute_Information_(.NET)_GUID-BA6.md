<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use Blocks and Attributes (.NET) > Work with Attributes (.NET) > Extract Attribute Information (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-BA69D85A-2AED-43C2-B5B7-73022B5F28F8.htm -->

# Extract Attribute Information (.NET)

You can extract attribute information from a block reference using the AttributeCollection property. The AttributeCollection property returns a collection of the attribute references attached to a block. When stepping through the collection, you can use the IsConstant property to see if an attributes value can be changed or not. 

You do not need template files to extract attribute information, and no attribute information files are created. Simply iterate the collection of attribute references, using the Tag and TextString properties of the attribute reference to examine the attribute information. You will also need to check to see if IsMTextAttribute is True or False, if True you will need to get the text value for the multiline attribute with the MTextAttribute property. 

For more information on extracting attribute information, see “About Extracting Data from Block Attributes” in the product Help system. 

## Get attribute reference information

This example creates a block and then adds an attribute to the block. The block is then inserted into the drawing. The attribute data is then returned and displayed using a message box. The attribute data is then updated for the block reference, and once again the attribute data is returned and displayed. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("GettingAttributes")]
    public void GettingAttributes()
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
    
            if (!acBlkTbl.Has("TESTBLOCK"))
            {
                using (BlockTableRecord acBlkTblRec = new BlockTableRecord())
                {
                    acBlkTblRec.Name = "TESTBLOCK";
    
                    // Set the insertion point for the block
                    acBlkTblRec.Origin = new Point3d(0, 0, 0);
    
                    // Add an attribute definition to the block
                    using (AttributeDefinition acAttDef = new AttributeDefinition())
                    {
                        acAttDef.Position = new Point3d(5, 5, 0);
                        acAttDef.Prompt = "Attribute Prompt";
                        acAttDef.Tag = "AttributeTag";
                        acAttDef.TextString = "Attribute Value";
                        acAttDef.Height = 1;
                        acAttDef.Justify = AttachmentPoint.MiddleCenter;
                        acBlkTblRec.AppendEntity(acAttDef);
    
                        acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForWrite);
                        acBlkTbl.Add(acBlkTblRec);
                        acTrans.AddNewlyCreatedDBObject(acBlkTblRec, true);
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
    
                using (BlockReference acBlkRef = new BlockReference(new Point3d(5, 5, 0), acBlkTblRec.Id))
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
    
                        // Display the tags and values of the attached attributes
                        string strMessage = "";
                        AttributeCollection attCol = acBlkRef.AttributeCollection;
    
                        foreach (ObjectId objID in attCol)
                        {
                            DBObject dbObj = acTrans.GetObject(objID, OpenMode.ForRead) as DBObject;
    
                            AttributeReference acAttRef = dbObj as AttributeReference;
    
                            strMessage = strMessage + "Tag: " + acAttRef.Tag + "\n" +
                                            "Value: " + acAttRef.TextString + "\n";
    
                            // Change the value of the attribute
                            acAttRef.TextString = "NEW VALUE!";
                        }
    
                        Application.ShowAlertDialog("The attributes for blockReference " + acBlkRef.Name + " are:\n" + strMessage);
    
                        strMessage = "";
                        foreach (ObjectId objID in attCol)
                        {
                            DBObject dbObj = acTrans.GetObject(objID, OpenMode.ForRead) as DBObject;
    
                            AttributeReference acAttRef = dbObj as AttributeReference;
    
                            strMessage = strMessage + "Tag: " + acAttRef.Tag + "\n" +
                                            "Value: " + acAttRef.TextString + "\n";
                        }
    
                        Application.ShowAlertDialog("The attributes for blockReference " + acBlkRef.Name + " are:\n" + strMessage);
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
    
    <CommandMethod("GettingAttributes")> _
    Public Sub GettingAttributes()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            Dim blkRecId As ObjectId = ObjectId.Null
    
            If Not acBlkTbl.Has("TESTBLOCK") Then
                Using acBlkTblRec As New BlockTableRecord
                    acBlkTblRec.Name = "TESTBLOCK"
    
                    ' Set the insertion point for the block
                    acBlkTblRec.Origin = New Point3d(0, 0, 0)
    
                    ' Add an attribute definition to the block
                    Using acAttDef As New AttributeDefinition
                        acAttDef.Position = New Point3d(5, 5, 0)
                        acAttDef.Prompt = "Attribute Prompt"
                        acAttDef.Tag = "AttributeTag"
                        acAttDef.TextString = "Attribute Value"
                        acAttDef.Height = 1
                        acAttDef.Justify = AttachmentPoint.MiddleCenter
                        acBlkTblRec.AppendEntity(acAttDef)
    
                        acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForWrite)
                        acBlkTbl.Add(acBlkTblRec)
                        acTrans.AddNewlyCreatedDBObject(acBlkTblRec, True)
                    End Using
    
                    blkRecId = acBlkTblRec.Id
                End Using
            Else
                blkRecId = acBlkTbl("TESTBLOCK")
            End If
    
            ' Create and insert the new block reference
            If blkRecId <> ObjectId.Null Then
                Dim acBlkTblRec As BlockTableRecord
                acBlkTblRec = acTrans.GetObject(blkRecId, OpenMode.ForRead)
    
                Using acBlkRef As New BlockReference(New Point3d(5, 5, 0), acBlkTblRec.Id)
    
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
    
                        ' Display the tags and values of the attached attributes
                        Dim strMessage As String = ""
                        Dim attCol As AttributeCollection = acBlkRef.AttributeCollection
    
                        For Each objID As ObjectId In attCol
                            Dim dbObj As DBObject = acTrans.GetObject(objID, OpenMode.ForRead)
    
                            Dim acAttRef As AttributeReference = dbObj
    
                            strMessage = strMessage & "Tag: " & acAttRef.Tag & vbCrLf & _
                                         "Value: " & acAttRef.TextString & vbCrLf
    
                            ' Change the value of the attribute
                            acAttRef.TextString = "NEW VALUE!"
                        Next
    
                        MsgBox("The attributes for blockReference " & acBlkRef.Name & " are: " & vbCrLf & strMessage)
                        strMessage = ""
    
                        For Each objID As ObjectId In attCol
                            Dim dbObj As DBObject = acTrans.GetObject(objID, OpenMode.ForRead)
    
                            Dim acAttRef As AttributeReference = dbObj
    
                            strMessage = strMessage & "Tag: " & acAttRef.Tag & vbCrLf & _
                                         "Value: " & acAttRef.TextString & vbCrLf
                        Next
    
                        MsgBox("The attributes for blockReference " & acBlkRef.Name & " are: " & vbCrLf & strMessage)
                    End If
                End Using
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub GettingAttributes()
        ' Create the block
        Dim blockObj As AcadBlock
        Dim insertionPnt(0 To 2) As Double
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        Set blockObj = ThisDrawing.Blocks.Add(insertionPnt, "TESTBLOCK")
     
        ' Define the attribute definition
        Dim attributeObj As AcadAttribute
        Dim height As Double
        Dim mode As Long
        Dim prompt As String
        Dim insertionPoint(0 To 2) As Double
        Dim tag As String
        Dim value As String
        height = 1
        prompt = "Attribute Prompt"
        insertionPoint(0) = 5
        insertionPoint(1) = 5
        insertionPoint(2) = 0
        tag = "AttributeTag"
        value = "Attribute Value"
     
        ' Create the attribute definition object on the block
        Set attributeObj = blockObj.AddAttribute(height, mode, prompt, insertionPoint, tag, value)
     
        ' Insert the block
        Dim blockRefObj As AcadBlockReference
        insertionPnt(0) = 2
        insertionPnt(1) = 2
        insertionPnt(2) = 0
        Set blockRefObj = ThisDrawing.ModelSpace.InsertBlock(insertionPnt, "TESTBLOCK", 1, 1, 1, 0)
    
        ' Get the attributes for the block reference
        Dim varAttributes As Variant
        varAttributes = blockRefObj.GetAttributes
     
        ' Move the attribute tags and values into a
        ' string to be displayed in a Msgbox
        Dim strAttributes As String
        strAttributes = ""
        Dim I As Integer
        For I = LBound(varAttributes) To UBound(varAttributes)
            strAttributes = strAttributes + "  Tag: " + _
            varAttributes(I).TagString + vbCrLf + _
            "   Value: " + varAttributes(I).textString
        Next
    
        MsgBox "The attributes for blockReference " + _
        blockRefObj.Name & " are: " & vbCrLf & strAttributes
     
        ' Change the value of the attribute
        ' Note: There is no SetAttributes. Once you have the
        ' variant array, you have the objects.
        ' Changing them changes the objects in the drawing.
        varAttributes(0).textString = "NEW VALUE!"
     
        ' Get the attributes again
        Dim newvarAttributes As Variant
        newvarAttributes = blockRefObj.GetAttributes
     
        ' Again, display the tags and values
        strAttributes = ""
        For I = LBound(varAttributes) To UBound(varAttributes)
            strAttributes = strAttributes + "  Tag: " + _
            newvarAttributes(I).TagString + vbCrLf + _
            "   Value: " + newvarAttributes(I).textString
        Next
    
        MsgBox "The attributes for blockReference " & _
        blockRefObj.Name & " are: " & vbCrLf & strAttributes
    End Sub
