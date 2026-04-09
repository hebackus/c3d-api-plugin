<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Selection Set Keywords (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-94A4E3DE-0066-4D6A-8558-0252BE8CB85E.htm -->

# Selection Set Keywords (.NET)

Applications may use keywords to prompt users for selection preferences before actually creating the selection set. 

Keywords can be assigned to an object selection operation by creating and instance of a PromptSelectionOptions object. After a PromptSelectionOptions object is created, the SetKeywords method is used to assign each individual keyword that the user can enter at the Command prompt. Once the keywords have been assigned to the PromptSelectionOptions object, the PromptSelectionOptions object must then be passed to the GetSelection method of the editor. 

The implementation of the keywords that a user can enter at the Select objects: prompt is handled with a PromptSelectionOptions.KeywordInput event handler. When the user enters a keyword at the resulting prompt, the KeywordInput event is raised and the application's handler is called. 

A KeywordInput handler receives a SelectionTextInputEventArgs argument that serves as both an input and output parameter. The Input property of the SelectionTextInputEventArgs argument indicates the keyword chosen. A typical handler compares this keyword to those in the application's keyword list and calls an appropriate selection method. If entities are returned by the selection method, the application adds these to the SelectionTextInputEventArgs argument with the SelectionTextInputEventArgs.AddObjects method. When the original GetSelection call returns, it provides the selected entities to the method that set the keyword list. 

The following example defines five keywords and adds a handler to support the keyword chosen by the user. 

## C#
    
    
    private static void SelectionKeywordInputHandler(object sender, SelectionTextInputEventArgs eSelectionInput)
    {
    			 // Gets the current document editor and define other variables for the current scope
    			 Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
        PromptSelectionResult acSSPrompt = null;
        SelectionSet acSSet = null;
        ObjectId[] acObjIds = null;
    
    	   // See if the user choose the myFence keyword
    	   switch (eSelectionInput.Input) {
            case "myFence":
    			         // Uses the four points to define a fence selection
                Point3dCollection ptsFence = new Point3dCollection();
                ptsFence.Add(new Point3d(5.0, 5.0, 0.0));
                ptsFence.Add(new Point3d(13.0, 15.0, 0.0));
                ptsFence.Add(new Point3d(12.0, 9.0, 0.0));
                ptsFence.Add(new Point3d(5.0, 5.0, 0.0));
    
                acSSPrompt = acDocEd.SelectFence(ptsFence);
    			         break;
            case "myWindow":
    			         // Defines a rectangular window selection
                acSSPrompt = acDocEd.SelectWindow(new Point3d(1.0, 1.0, 0.0), new Point3d(30.0, 20.0, 0.0));
    			         break;
            case "myWPoly":
    			         // Uses the four points to define a polygon window selection
                Point3dCollection ptsPolygon = new Point3dCollection();
                ptsPolygon.Add(new Point3d(5.0, 5.0, 0.0));
                ptsPolygon.Add(new Point3d(13.0, 15.0, 0.0));
                ptsPolygon.Add(new Point3d(12.0, 9.0, 0.0));
                ptsPolygon.Add(new Point3d(5.0, 5.0, 0.0));
    
                acSSPrompt = acDocEd.SelectWindowPolygon(ptsPolygon);
    			         break;
    		      case "myLastSel":
    			        // Gets the last object created
    			        acSSPrompt = acDocEd.SelectLast();
    			        break;
    		      case "myPrevSel":
    			        // Gets the previous object selection set
    			        acSSPrompt = acDocEd.SelectPrevious();
    			        break;
    	   }
    
        // If the prompt status is OK, objects were selected and return
        if (acSSPrompt != null)
        {
            if (acSSPrompt.Status == PromptStatus.OK)
            {
                // Objects were selected, so add them to the current selection
                acSSet = acSSPrompt.Value;
                acObjIds = acSSet.GetObjectIds();
                eSelectionInput.AddObjects(acObjIds);
            }
        }
    }
    
    [CommandMethod("SelectionKeywordInput")]
    public static void SelectionKeywordInput()
    {
        // Gets the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Setups the keyword options
        PromptSelectionOptions acKeywordOpts = new PromptSelectionOptions();
        acKeywordOpts.Keywords.Add("myFence");
        acKeywordOpts.Keywords.Add("myWindow");
        acKeywordOpts.Keywords.Add("myWPoly");
        acKeywordOpts.Keywords.Add("myLastSel");
        acKeywordOpts.Keywords.Add("myPrevSel");
    
        // Adds the event handler for keyword input
        acKeywordOpts.KeywordInput += new SelectionTextInputEventHandler(SelectionKeywordInputHandler);
    
        // Prompts the user for a selection set
        PromptSelectionResult acSSPrompt = acDocEd.GetSelection(acKeywordOpts);
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            // Gets the selection set
            SelectionSet acSSet = acSSPrompt.Value;
    
            // Gets the objects from the selection set
            ObjectId[] acObjIds = acSSet.GetObjectIds();
            Database acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
            // Starts a transaction
            using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
            {
                try
                {
                    // Gets information about each object
                    foreach (ObjectId acObjId in acObjIds)
                    {
                        Entity acEnt = (Entity)acTrans.GetObject(acObjId, OpenMode.ForWrite, true);
                        acDocEd.WriteMessage("\nObject selected: " + acEnt.GetType().FullName);
    
                    }
                }
                finally
                {
                    acTrans.Dispose();
                }
            }
        }
    
        // Removes the event handler for keyword input
        acKeywordOpts.KeywordInput -= new SelectionTextInputEventHandler(SelectionKeywordInputHandler);
    }

## VB.NET
    
    
    Private Shared Sub SelectionKeywordInputHandler(ByVal sender As Object, ByVal eSelectionInput As SelectionTextInputEventArgs)
        '' Gets the current document editor and define other variables for the current scope
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
        Dim acSSPrompt As PromptSelectionResult = Nothing
    
        '' See if the user choose the myFence keyword
        Select Case eSelectionInput.Input
            Case "myFence"
                '' Uses the four points to define a fence selection
                Dim ptsFence As New Point3dCollection()
                ptsFence.Add(New Point3d(5.0, 5.0, 0.0))
                ptsFence.Add(New Point3d(13.0, 15.0, 0.0))
                ptsFence.Add(New Point3d(12.0, 9.0, 0.0))
                ptsFence.Add(New Point3d(5.0, 5.0, 0.0))
    
                acSSPrompt = acDocEd.SelectFence(ptsFence)
            Case "myWindow"
                '' Defines a rectangular window selection
                acSSPrompt = acDocEd.SelectWindow(New Point3d(1.0, 1.0, 0.0), _
                                                  New Point3d(30.0, 20.0, 0.0))
            Case "myWPoly"
                '' Uses the four points to define a polygon window selection
                Dim ptsPolygon As New Point3dCollection()
                ptsPolygon.Add(New Point3d(5.0, 5.0, 0.0))
                ptsPolygon.Add(New Point3d(13.0, 15.0, 0.0))
                ptsPolygon.Add(New Point3d(12.0, 9.0, 0.0))
                ptsPolygon.Add(New Point3d(5.0, 5.0, 0.0))
    
                acSSPrompt = acDocEd.SelectWindowPolygon(ptsPolygon)
            Case "myLastSel"
                '' Gets the last object created
                acSSPrompt = acDocEd.SelectLast()
            Case "myPrevSel"
                '' Gets the previous object selection set
                acSSPrompt = acDocEd.SelectPrevious()
        End Select
    
        '' If the prompt status is OK, objects were selected
        If Not acSSPrompt Is Nothing Then
            If acSSPrompt.Status = PromptStatus.OK Then
                '' Objects were selected, so add them to the current selection
                Dim acSSet As SelectionSet = acSSPrompt.Value
                Dim acObjIds As ObjectId() = acSSet.GetObjectIds()
                eSelectionInput.AddObjects(acObjIds)
            Else
                Return
            End If
        End If
    End Sub
    
    <CommandMethod("SelectionKeywordInput")> _
    Public Sub SelectionKeywordInput()
        '' Gets the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Setups the keyword options
        Dim acKeywordOpts As New PromptSelectionOptions()
        acKeywordOpts.Keywords.Add("myFence")
        acKeywordOpts.Keywords.Add("myWindow")
        acKeywordOpts.Keywords.Add("myWPoly")
        acKeywordOpts.Keywords.Add("myLastSel")
        acKeywordOpts.Keywords.Add("myPrevSel")
    
        '' Adds the event handler for keyword input
        AddHandler acKeywordOpts.KeywordInput, AddressOf SelectionKeywordInputHandler
    
        '' Prompts the user for a selection set
        Dim acSSPrompt As PromptSelectionResult = acDocEd.GetSelection(acKeywordOpts)
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            '' Gets the selection set
            Dim acSSet As SelectionSet = acSSPrompt.Value
    
            '' Gets the objects from the selection set
            Dim acObjIds As ObjectId() = acSSet.GetObjectIds()
            Dim acCurDb As Database = Application.DocumentManager.MdiActiveDocument.Database
    
            '' Starts a transaction
            Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
                Try
                    '' Gets information about each object
                    For Each acObjId As ObjectId In acObjIds
                        Dim acEnt As Entity = acTrans.GetObject(acObjId, OpenMode.ForWrite, True)
                        acDocEd.WriteMessage(vbLf + "Object selected: " + acEnt.GetType().FullName)
                    Next acObjId
                Finally
                    acTrans.Dispose()
                End Try
            End Using
        End If
    
        '' Removes the event handler for keyword input
        RemoveHandler acKeywordOpts.KeywordInput, AddressOf SelectionKeywordInputHandler
    End Sub
