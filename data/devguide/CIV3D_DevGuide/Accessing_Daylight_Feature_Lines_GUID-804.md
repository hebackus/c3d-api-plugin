<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Parcels > Accessing Daylight Feature Lines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-804AA1FB-1DE2-4784-8039-CAB85BEE1C6F.htm -->

# Accessing Daylight Feature Lines

The AeccSite:FeatureLines property is a collection of grading feature lines in the drawing. This collection only contains the types of feature lines available through the Prospector on the Autodesk Civil 3D user interface. The collection doesn’t contain daylight or projection feature lines. However, you can still get information about these types of feature lines programmatically by prompting the user to select feature line object in a drawing. This code sample prompts the user to select a feature line, and then prints out the number of points it contains:
    
    
    Dim objPart As AeccLandFeatureLine
    Dim objEnt As AcadObject
    Dim objAcadEnt As AcadEntity
    Dim varPick As Variant
    ThisDrawing.Utility.GetEntity objEnt, varPick, "Select the polyline/feature line"
    If TypeOf objEnt Is AeccLandFeatureLine Then
       Set objPart = objEnt
       Debug.Print TypeName(objPart)
       Dim varArray As Variant
       varArray = objPart.GetPoints()
       Debug.Print "Number of points = " & UBound(varArray)
    ElseIf TypeOf objEnt Is AcadEntity Then
       Set objAcadEnt = objEnt
       Debug.Print TypeName(objAcadEnt)
       If (g_oAeccDoc.Sites.Count = 0) Then
          g_oAeccDoc.Sites.Add "TestSite"
       End If
       Set objPart = g_oAeccDoc.Sites(0).FeatureLines.AddFromPolyline(objAcadEnt.ObjectID, "Standard")
    End If
