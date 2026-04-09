<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Getting Survey Network Drawing Objects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-18583E20-F6B9-4118-913C-C1798F2124F5.htm -->

# Getting Survey Network Drawing Objects

You can get and manipulate the AutoCAD drawing objects that make up a survey network from the Autodesk Civil 3D user interface. The drawing objects are represented by the AeccSurveyNetworkEntity object. For example, this code prompts the user to select the survey network, tests whether it is the survey network object, and then prints some information about it:
    
    
    Dim objPart As AeccSurveyNetworkEntity
    Dim objEnt As AcadObject
    Dim objAcadEnt As AcadEntity
    Dim varPick As Variant
    ThisDrawing.Utility.GetEntity objEnt, varPick, "Select the Survey Network"
    If TypeOf objEnt Is AeccSurveyNetworkEntity Then
       Set objPart = objEnt
       Debug.Print objPart.Name, TypeName(objPart)
    ElseIf TypeOf objEnt Is AcadEntity Then
       Set objAcadEnt = objEnt
       Debug.Print objAcadEnt.Name, TypeName(objAcadEnt)
    End If
