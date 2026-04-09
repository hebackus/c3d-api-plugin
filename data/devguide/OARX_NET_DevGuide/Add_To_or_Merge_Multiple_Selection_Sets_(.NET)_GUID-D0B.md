<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Add To or Merge Multiple Selection Sets (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D0BD4249-1122-4209-ABEA-6F19FA156F91.htm -->

# Add To or Merge Multiple Selection Sets (.NET)

You can merge multiple selection sets be creating an ObjectIdCollection object and then adding the object ids from multiple selection sets together. In addition to adding object ids to an ObjectIdCollection object, you can remove object ids. Once all object ids are added to an ObjectIdCollection object, you can iterate through the collection of object ids and manipulate each object as needed. 

## Add selected objects to a selection set

This example prompts the user to select objects twice and then merges the two selection sets created into a single selection set. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("MergeSelectionSets")]
    public static void MergeSelectionSets()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Request for objects to be selected in the drawing area
        PromptSelectionResult acSSPrompt;
        acSSPrompt = acDocEd.GetSelection();
    
        SelectionSet acSSet1;
        ObjectIdCollection acObjIdColl = new ObjectIdCollection();
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            // Get the selected objects
            acSSet1 = acSSPrompt.Value;
    
            // Append the selected objects to the ObjectIdCollection
            acObjIdColl = new ObjectIdCollection(acSSet1.GetObjectIds());
        }
    
        // Request for objects to be selected in the drawing area
        acSSPrompt = acDocEd.GetSelection();
    
        SelectionSet acSSet2;
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            acSSet2 = acSSPrompt.Value;
    
            // Check the size of the ObjectIdCollection, if zero, then initialize it
            if (acObjIdColl.Count == 0)
            {
                acObjIdColl = new ObjectIdCollection(acSSet2.GetObjectIds());
            }
            else
            {
                // Step through the second selection set
                foreach (ObjectId acObjId in acSSet2.GetObjectIds())
                {
                    // Add each object id to the ObjectIdCollection
                    acObjIdColl.Add(acObjId);
                }
            }
        }
    
        Application.ShowAlertDialog("Number of objects selected: " +
                                    acObjIdColl.Count.ToString());
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("MergeSelectionSets")> _
    Public Sub MergeSelectionSets()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Request for objects to be selected in the drawing area
        Dim acSSPrompt As PromptSelectionResult
        acSSPrompt = acDocEd.GetSelection()
    
        Dim acSSet1 As SelectionSet
        Dim acObjIdColl As ObjectIdCollection = New ObjectIdCollection()
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            '' Get the selected objects
            acSSet1 = acSSPrompt.Value
    
            '' Append the selected objects to the ObjectIdCollection
            acObjIdColl = New ObjectIdCollection(acSSet1.GetObjectIds())
        End If
    
        '' Request for objects to be selected in the drawing area
        acSSPrompt = acDocEd.GetSelection()
    
        Dim acSSet2 As SelectionSet
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            acSSet2 = acSSPrompt.Value
    
            '' Check the size of the ObjectIdCollection, if zero, then initialize it
            If acObjIdColl.Count = 0 Then
                acObjIdColl = New ObjectIdCollection(acSSet2.GetObjectIds())
            Else
                Dim acObjId As ObjectId
    
                '' Step through the second selection set
                For Each acObjId In acSSet2.GetObjectIds()
                    '' Add each object id to the ObjectIdCollection
                    acObjIdColl.Add(acObjId)
                Next
            End If
        End If
    
        Application.ShowAlertDialog("Number of objects selected: " & _
                                    acObjIdColl.Count.ToString())
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub MergeSelectionSets()
        ' Create a new selection set
        Dim sset As AcadSelectionSet
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        ' Prompt the user to select objects
        ' and add them to the selection set.
        sset.SelectOnScreen
     
        ' Prompt the user again to select objects
        ' and add them to the same selection set.
        sset.SelectOnScreen
     
        MsgBox "Number of total objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub
