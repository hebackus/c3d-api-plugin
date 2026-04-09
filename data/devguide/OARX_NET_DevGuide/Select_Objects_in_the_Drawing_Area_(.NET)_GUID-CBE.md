<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Select Objects in the Drawing Area (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CBECEDCF-3B4E-4DF3-99A0-47103D10DADD.htm -->

# Select Objects in the Drawing Area (.NET)

You can select objects through by having the user interactively select objects, or you can simulate many of the various object selection options through the AutoCAD .NET API. If your routine performs multiple selection sets, you will need to either track each selection set returned or create an ObjectIdCollection object to keep track of all the selected objects. The following functions allow you to select objects from the drawing: 

GetSelection
    

Prompts the user to pick objects from the screen. 

SelectAll
    

Selects all the objects in the drawing. 

Note: Objects in all layouts and spaces are selected, and objects that are locked or frozen. 

SelectCrossingPolygon
    

Selects objects within and crossing a polygon defined by specifying points. The polygon can be any shape but cannot cross or touch itself. 

SelectCrossingWindow
    

Selects objects within and crossing an area defined by two points. 

SelectFence
    

Selects all objects crossing a selection fence. Fence selection is similar to crossing polygon selection except that the fence is not closed, and a fence can cross itself. 

SelectLast
    

Selects the last object created in the current space. 

SelectPrevious
    

Selects all objects selected during the previous Select objects: prompt. 

SelectWindow
    

Selects all objects completely inside a rectangle defined by two points. 

SelectWindowPolygon
    

Selects objects completely inside a polygon defined by points. The polygon can be any shape but cannot cross or touch itself. 

SelectAtPoint
    

Selects objects passing through a given point and places them into the active selection set. 

SelectByPolygon
    

Selects objects within a fence and adds them to the active selection set. 

## Prompt for objects on screen and iterate the selection set

This example prompts the user to select objects, then changes the color of each object selected to Green or the AutoCAD Color Index of 3. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("SelectObjectsOnscreen")]
    public static void SelectObjectsOnscreen()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Request for objects to be selected in the drawing area
            PromptSelectionResult acSSPrompt = acDoc.Editor.GetSelection();
    
            // If the prompt status is OK, objects were selected
            if (acSSPrompt.Status == PromptStatus.OK)
            {
                SelectionSet acSSet = acSSPrompt.Value;
    
                // Step through the objects in the selection set
                foreach (SelectedObject acSSObj in acSSet)
                {
                    // Check to make sure a valid SelectedObject object was returned
                    if (acSSObj != null)
                    {
                        // Open the selected object for write
                        Entity acEnt = acTrans.GetObject(acSSObj.ObjectId,
                                                         OpenMode.ForWrite) as Entity;
    
                        if (acEnt != null)
                        {
                            // Change the object's color to Green
                            acEnt.ColorIndex = 3;
                        }
                    }
                }
    
                // Save the new object to the database
                acTrans.Commit();
            }
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("SelectObjectsOnscreen")> _
    Public Sub SelectObjectsOnscreen()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Request for objects to be selected in the drawing area
            Dim acSSPrompt As PromptSelectionResult = acDoc.Editor.GetSelection()
    
            '' If the prompt status is OK, objects were selected
            If acSSPrompt.Status = PromptStatus.OK Then
                Dim acSSet As SelectionSet = acSSPrompt.Value
    
                '' Step through the objects in the selection set
                For Each acSSObj As SelectedObject In acSSet
                    '' Check to make sure a valid SelectedObject object was returned
                    If Not IsDBNull(acSSObj) Then
                        '' Open the selected object for write
                        Dim acEnt As Entity = acTrans.GetObject(acSSObj.ObjectId, _
                                                                OpenMode.ForWrite)
    
                        If Not IsDBNull(acEnt) Then
                            '' Change the object's color to Green
                            acEnt.ColorIndex = 3
                        End If
                    End If
                Next
    
                '' Save the new object to the database
                acTrans.Commit()
            End If
    
            '' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SelectObjectsOnscreen()
        ' Create a new selection set
        Dim sset As AcadSelectionSet
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        ' Prompt the user to select objects
        ' and add them to the selection set.
        sset.SelectOnScreen
     
        Dim acEnt As AcadEntity
     
        ' Step through the selected objects and change
        ' each object's color to Green
        For Each acEnt In sset
            ' Use the Color property to set the object's color
            acEnt.color = acGreen
        Next acEnt
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub

## Select objects with crossing window

This example selects the objects within and that intersect a crossing window. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("SelectObjectsByCrossingWindow")]
    public static void SelectObjectsByCrossingWindow()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Create a crossing window from (2,2,0) to (10,8,0)
        PromptSelectionResult acSSPrompt;
        acSSPrompt = acDocEd.SelectCrossingWindow(new Point3d(2, 2, 0),
                                                  new Point3d(10, 8, 0));
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            SelectionSet acSSet = acSSPrompt.Value;
    
            Application.ShowAlertDialog("Number of objects selected: " +
                                        acSSet.Count.ToString());
        }
        else
        {
            Application.ShowAlertDialog("Number of objects selected: 0");
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("SelectObjectsByCrossingWindow")> _
    Public Sub SelectObjectsByCrossingWindow()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Create a crossing window from (2,2,0) to (10,8,0)
        Dim acSSPrompt As PromptSelectionResult
        acSSPrompt = acDocEd.SelectCrossingWindow(New Point3d(2, 2, 0), _
                                                  New Point3d(10, 8, 0))
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            Dim acSSet As SelectionSet = acSSPrompt.Value
    
            Application.ShowAlertDialog("Number of objects selected: " & _
                                        acSSet.Count.ToString())
        Else
            Application.ShowAlertDialog("Number of objects selected: 0")
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SelectObjectsByCrossingWindow()
        ' Create a new selection set
        Dim sset As AcadSelectionSet
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        ' Define the points for the crossing window
        Dim pt1(0 To 2) As Double
        Dim pt2(0 To 2) As Double
     
        pt1(0) = 2#: pt1(1) = 2#: pt1(2) = 0#:
        pt2(0) = 10#: pt2(1) = 8#: pt2(2) = 0#:
     
        ' Create a crossing window from (2,2,0) to (10,8,0)
        sset.Select acSelectionSetCrossing, pt1, pt2
     
        MsgBox "Number of objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub
