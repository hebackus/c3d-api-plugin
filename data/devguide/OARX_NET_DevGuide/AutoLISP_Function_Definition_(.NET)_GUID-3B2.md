<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Define Commands and AutoLISP Functions (.NET) > AutoLISP Function Definition (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3B2760FE-A0DC-4229-AEBE-5CC83290BA95.htm -->

# AutoLISP Function Definition (.NET)

When defining an AutoLISP function, you use the LispFunction attribute. The LispFunction attribute expects a string value to use as the global name of the AutoLISP function that is being defined. Along with a global function name, the LispFunction structure can accept the following values: 

  * **Local Name** \- Local function name, usually language specific 
  * **Help Topic Name** \- Help topic name that should be associated with the AutoLISP function 
  * **Help File Name** \- Help file that contains the help topic that should be displayed when the command is active and F1 is pressed 

## Syntax to Define an AutoLISP Function

The following demonstrates the creation of a LispFunction attribute that defines an AutoLISP function named InsertDynamicBlock. 

### C#
    
    
    [LispFunction("DisplayFullName")]
    public static void DisplayFullName(ResultBuffer rbArgs)
    {
     . . .
    }

### VB.NET
    
    
    <LispFunction("InsertDynamicBlock")> _
    Public Sub InsertDynamicBlock(ByVal rbArgs As ResultBuffer)
     . . .
    End Sub

## Retrieve Values Passed into an AutoLISP Function

Use a Foreach loop to step through the values returned in the ResultBuffer by the AutoLISP function. A ResultBuffer is a collection of TypedValue objects. The TypeCode property of a TypedValue object can be used to determine the value type for each value passed into the AutoLISP function. The Value property is used to return the value of the TypedValue object. 

The data types supported are: 

  * Boolean or bool 
  * Double or double 
  * Integer or int 
  * Null or void 
  * ObjectId 
  * Point2d 
  * Point3d 
  * ResultBuffer 
  * SelectionSet 
  * String or string 
  * TypedValue 

## To define an AutoLISP Function

This example code defines an AutoLISP function named DisplayFullName. While the method defined in the .NET project accepts a single value, the AutoLISP function expects two string values to produce the correct output. 

Load the .NET project into AutoCAD and enter the following at the Command prompt: 
    
    
    (displayfullname "First" "Last")

The following is the output displayed after the AutoLISP function is executed: 
    
    
    Name: First Last

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
     
    [LispFunction("DisplayFullName")]
    public static void DisplayFullName(ResultBuffer rbArgs)
    {
      if (rbArgs != null)
      {
          string strVal1 = "";
          string strVal2 = "";
     
          int nCnt = 0;
          foreach (TypedValue rb in rbArgs)
          {
              if (rb.TypeCode == (int)Autodesk.AutoCAD.Runtime.LispDataType.Text)
              {
                  switch(nCnt)
                  {
                      case 0:
                          strVal1 = rb.Value.ToString();
                          break;
                      case 1:
                          strVal2 = rb.Value.ToString();
                          break;
                  }
     
                  nCnt = nCnt + 1;
              }
          }
     
          Application.DocumentManager.MdiActiveDocument.Editor.
             WriteMessage("\nName: " + strVal1 + " " + strVal2);
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
     
    <LispFunction("DisplayFullName")> _
    Public Sub DisplayFullName(ByVal rbArgs As ResultBuffer)
      If Not rbArgs = Nothing Then
          Dim strVal1 As String = "", strVal2 As String = ""
     
          Dim nCnt As Integer = 0
          For Each rb As TypedValue In rbArgs
              If (rb.TypeCode = Autodesk.AutoCAD.Runtime.LispDataType.Text) Then
                  Select Case nCnt
                      Case 0
                          strVal1 = rb.Value.ToString()
                      Case 1
                          strVal2 = rb.Value.ToString()
                  End Select
     
                  nCnt = nCnt + 1
              End If
          Next
     
          Application.DocumentManager.MdiActiveDocument.Editor. _
             WriteMessage(vbLf & "Name: " & strVal1 & " " & strVal2)
      End If
    End Sub
