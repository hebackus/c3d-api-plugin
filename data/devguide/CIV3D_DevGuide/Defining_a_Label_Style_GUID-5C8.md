<!-- Developer's Guide > API Developer's Guide > Root Objects and Common Concepts > Label Styles > Defining a Label Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5C8D107C-8E28-49F9-8B3A-84F0BB87F77B.htm -->

# Defining a Label Style

A label style consists of collections of different features of a label, called “components”. The collection of these components is accessed with the LabelStyle::GetComponents() method, which takes the type (LabelStyleComponentType) of component to get. The component types are:

  * Text
  * Line
  * Block \- symbols
  * Tick \- for both major and minor tick marks
  * ReferenceText
  * DirectionArrow
  * TextForEach

Not all of these may be valid, depending on the label style type. For example, adding a tick mark component to a label style meant for a point has no visible effect. Label styles also depend on graphical objects that may or may not be part of the current document. For example, if the style references a block that is not part of the current document, then the specified block or tick components are not shown.

To add a feature to a label style, add a new component to the corresponding collection using the LabelStyle::AddComponent() method. Then set the properties of that component to the appropriate values. Always make sure to set the Visible property to true.
    
    
    try
    {
        // Add a line to the collection of lines in our label style
        ObjectId lineComponentId = oLabelStyle.AddComponent("New Line Component", LabelStyleComponentType.Line);
        // Get the new component:
        ObjectIdCollection lineCompCol = oLabelStyle.GetComponents(LabelStyleComponentType.Line);
        var newLineComponent = ts.GetObject(lineComponentId, OpenMode.ForWrite) as LabelStyleLineComponent;
        // Now we can modify the component
        newLineComponent.General.Visible.Value = true;
        newLineComponent.Line.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 40); // orange-yellow
        newLineComponent.Line.Angle.Value = 2.094; // radians, = 120 deg
        // negative lengths are allowed - they mean the line is drawn
        // in the opposite direction to the angle specified:
        newLineComponent.Line.Length.Value = -0.015;
        newLineComponent.Line.StartPointXOffset.Value = 0.005;
        newLineComponent.Line.StartPointYOffset.Value = -0.005;
    }
    // Thrown if component isn't valid, or name is duplicated
    catch (System.ArgumentException e)
    {
        Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("Error: {0}\n", e.Message);
    }
    

When first created, the label style object is set according to the ambient settings. Because of this, a new label style object may already contain features. If you are creating a new label style object, be sure to check for such existing features or your style might contain unintended elements.
    
    
    // Check to see whether any text components already exist.  
    // If not, add one.  
    if (oLabelStyle.GetComponentsCount(LabelStyleComponentType.Text) == 0)
    {
        // Add a text component 
        oLabelStyle.AddComponent("New Text ", LabelStyleComponentType.Text);
    }
    // Now modify the first one:
    ObjectIdCollection textCompCol = oLabelStyle.GetComponents(LabelStyleComponentType.Text);
    var newTextComponent = ts.GetObject(textCompCol[0], OpenMode.ForWrite) as LabelStyleTextComponent;
    

The ambient settings also define which units are used. If you are creating an application designed to work with different drawings, you should take ambient settings into account or labels may demonstrate unexpected behavior in each document.
