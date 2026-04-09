<!-- Developer's Guide > API Developer's Guide > Converting VBA Subassemblies to .NET > Procedure > Port the VBA Code to Visual Basic .NET Code -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E90C4F80-8921-434D-9D66-DD373B463C9D.htm -->

# Port the VBA Code to Visual Basic .NET Code

Now begin the porting work. The following sections outline the main steps in porting. Code from the stock subassembly DaylightBench.vb is used as an illustration.

## Step 1: Import the necessary namespaces 

Adding the namespaces Autodesk.Civil.Roadway and Autodesk.Civil is recommended because members in these two namespaces are frequently used in subassemblies. Your subassembly may require additional namespaces. These are the namespaces imported in the stock Civil 3D subassemblies (from C3DStockSubassemblies.vbproj):

  * Autodesk.Civil
  * Autodesk.Civil.ApplicationServices
  * Autodesk.Civil.DatabaseServices
  * Autodesk.Civil.Land
  * Autodesk.Civil.Land.DatabaseServices
  * Autodesk.Civil.Land.Settings
  * Autodesk.Civil.Roadway
  * Autodesk.Civil.Roadway.DatabaseServices
  * Autodesk.Civil.Roadway.Settings
  * Autodesk.Civil.Runtime
  * Autodesk.Civil.Settings

## Step 2: Remove all  On Error… statements

Remove the On Error statements in the GetLogicalNamesImplement(), GetInputParametersImplement(), and GetOutputParametersImplement() methods. Comment these statements out in DrawImplement (), because you will re-use the code in Step 14. 

Regular expression:

  * Find: On Error{.*}
  * Leave the Replace field blank if you want to delete these statements. Use ' On Error\1 if you only want to comment them out.

## Step 3: Remove  Exit Sub and  Error Handler

Remove all the Exit Sub and Error Handler: statements at the end of each subroutine. In VBA, you may see following code at the end of each subroutine - remove it, or move it into the appropriate Catch statement when converting error handling logic in step 14.
    
    
    Exit Sub
    ErrorHandler:
    RecordError Err.Number, Err.Description, Err.Source
    

Regular expression:

  * Find: Exit Sub{ *}\n{ *}\n{ *}ErrorHandler\:{ *}\n{ *}RecordError.+{ *}\n{ *}{End Sub}
  * Replace: \8

## Step 4: Remove  oRwyState definition.

Remove the following code at the beginning of each subroutine:
    
    
    ' Get the roadway state object
    Dim oRwyState As AeccRoadwayState
    Set oRwyState = GetRoadwayState()
    

The corridorState object is already passed in by the argument of the subroutine, so it is not necessary to get it yourself.

Regular expression:

  * Find: {'.*}{ *}\n{ +}Dim.+As AeccRoadwayState{ *}\n{ *}.+= GetRoadwayState\\(\\)
  * Replace: leave blank to delete these statements

## Step 5: Replace  oRwyState with  corridorState

All instances of the variable oRwyState used in VBA should be renamed corridorState in .NET. The corridorState variable is passed in by argument. 

Regular expression:

  * Find: oRwyState
  * Replace: corridorState

## Step 6: Check for errors when accessing parameter values

In VBA, the parameter Value() method returns null if the key does not exist. In the .NET API, the same code will throw an exception. Where you access a parameter, you need to use a Try / Catch block to catch this case:
    
    
    ' VBA:
    vCutSlope = oParamsDouble.Value("CutSlope")
    If IsEmpty(vCutSlope) Then vCutSlope = c_dCutSlopeDefault
    

This code can be changed to:
    
    
    ' .NET:
    Try
        vCutSlope = oParamsDouble.Value("CutSlope ")
    Catch
        vCutSlope = c_ dCutSlopeDefault
    End Try
    

Regular expression:

  * Find: ^{.+ =.+\\.Value\\(.+\\)}\n{ +}If IsEmpty.+Then{.+}
  * Replace: Try\n\1\nCatch\n\3\nEnd Try\n

## Step 7: Update  RecordError()

The global function RecordError() is replaced by Utilities.RecordError().
    
    
    ' VBA:
    RecordError(aeccRoadwayErrorValueTooLarge, "RoundingTesselation", "DaylightBench")
    

Change to:
    
    
    '.NET:
    Utilities.RecordError(corridorState, CorridorError.ValueTooLarge, "RoundingTesselation", "DaylightBench")
    

Regular expression:

  * Find: {Record}{Warning|Error}{\\(}{aecc}{RoadwayError}
  * Replace: Utilities.Record\2\3roadwayState,RoadwayError.

## Step 8: Replace global variables with  Utilities variables.

In VBA subassembly code, you will see global variables such as g_iRight, g_sSide, which have a "g_" prefix. Most of these global variables have been moved to the Utilities class and renamed.

The following table lists some commonly used global variables and their corresponding ones in the Utilities class. Refer to the definition of the Utilities class for more information. 

From | To  
---|---  
g_sSide |  Utilities.Side  
g_iLeft |  Utilities.Left  
g_iRight |  Utilities.Right  
g_iTrue |  Utilities.ITrue  
Rounding_Option.NoneType |  Utilities.RoundingOption.NoneType  
CutSituation |  Utilities.FillOrCut.FillSituation  
SubbaseType |  Utilities.ShoulderSubbaseType.Subbase  
  
## Step 9: Rename enumerations 

In VBA subassembly code, nearly all the COM enumerations have an "aecc" prefix, such as aeccParamLogicalNameTypeAlignment. Replace them with corresponding .NET enumerations.

As a rule, the corresponding .NET enumerations are named by removing the "aecc" prefix and making the detail category a child member. For example, aeccParamLogicalNameTypeAlignment becomes ParamLogicalNameType.Alignment. 

The following table lists some commonly used COM enumerations and their corresponding .NET enumerations. 

From | To  
---|---  
aeccParamLogicalNameTypeAlignment |  ParamLogicalNameType.Alignment  
aeccRoadwayModeLayout |  CorridorMode.Layout  
aeccParamAccessOutput |  ParamAccessType.Output  
  
## Step 10: Rename types 

Replace COM types with their corresponding .NET types.

The following table lists some commonly used COM types and their corresponding .NET types.

From | To  
---|---  
IAeccParamsDouble |  ParamDoubleCollection  
IAeccRoadwayLinks |  LinkCollection  
IAeccParam |  Param  
AeccRoadwayLink |  Link  
AeccParamLong |  ParamLong  
  
Regular expressions:

  1. Convert  IAeccParamsAlignment and  AeccParamsAlignment to  ParamAlignmentCollection

     * Find: { }I*AeccParams{.+}{ |\n}
     * Replace: \1Param\2Collection\3
  2. Convert:  IAeccRoadwayLinks to  LinkCollection

     * Find: { }I*AeccRoadway{.*}s{ |\n}
     * Replace: \1\2Collection\3
  3. Convert  AeccRoadwayLink to  Link

     * Find: { }(I|())AeccRoadway{Link|Shape}{ |\n}
     * Replace: \1\2\3
  4. Convert  AeccParamLong to  ParamLong

     * Find: { }I*AeccParam{Long|Bool|Double|Point|String|()}{ |\n}
     * Replace: \1Param\2\3

These four regular expressions do not cover all the required changes, so you will have to make additional changes manually.

## Step 11: Change  Object to build-in types

Where the subassembly uses Object, it should be changed to a built-in type, as Object is not type-safe.
    
    
    ' .NET Before:
    Dim vSide As Object
    Try
          vSide = oParamsLong.Value(Utilities.Side)
    Catch
          vSide = SideDefault
    End Try
    
    
    
    ' .NET After:
    Dim vSide As Long
    Try
          vSide = oParamsLong.Value(Utilities.Side)
    Catch
          vSide = SideDefault
    End Try
    

## Step 12: Update code variables to use .NET naming

Remove the g_All, g_s and s prefixes in each variable name to match the new convention for code names.

From | To  
---|---  
g_AllCodes.g_sHinge_Cut.sCode |  Codes.HingeCut.Code  
g_AllCodes.g_sDaylight.sCode |  Codes.Daylight.Code  
g_AllCodes.g_sDaylight_Cut.sCode |  Codes.DaylightCut.Code  
  
Regular expression:

  * Find: g_All{Codes\\.}g_s{.+\\.}s{.+}
  * Replace: \1\2\3

## Step 13: Update array definitions

In VBA, many arrays are defined with a lower bound at index “1”. This is not allowed in .NET, so you should modify their definitions.

In most situations, you can just modify the array definition do not need to make any other changes. The array element 0 is defined but left unused. 
    
    
    ' .NET Before:
    Dim sPointCodeArray(1 To 9, 0 To 1) As String
    
    
    
    ' .NET After:
    Dim sPointCodeArray(0 To 9, 0 To 1) As String
    

If this array is passed as an argument to a method, you will need to do more work. In this case, the array is most likely used from index “0”. You need to modify all the code that uses this array to take into account the change in index numbering.

## Step 14: Modify error handling

In VBA, On Error Resume Next and On Error GoTo ErrorHandler statements are used to handle errors. But in .NET, exceptions are used instead. Modify all cases where errors are detected to use Try…Catch blocks.
    
    
    ' VBA:
    On Error Resume Next
    Dim oTargetDTM As IAeccSurface
    Set oTargetDTM = oParamsSurface.Value("TargetDTM")
    If oTargetDTM Is Nothing Then
        ' Error handling code goes here
        Exit Sub
    End If
    On Error GoTo ErrorHandler
    

Change error handling to:
    
    
    ' .NET:
    Dim oTargetDTMId As ObjectId
    Try
        oTargetDTMId = oParamsSurface.Value("TargetDTM")
    Catch
          ' Error handling code goes here
        Exit Sub
    End Try
    

## Step 15: New rules for database objects

In the COM API, the arguments and return values all refer to a database object instance. However, in the .NET API, arguments and return values are the ObjectId of the database object, not the object itself.
    
    
    ' VBA:
    Dim oTargetDTM As IAeccSurface
    Set oTargetDTM = oParamsSurface.Value("TargetDTM")
    

In .NET this would be:
    
    
    ' .NET:
    Dim oTargetDTMId As ObjectId
    Try
       oTargetDTMId = oParamsSurface.Value("TargetDTM")
    Catch	
    End Try
    

Then, to use the database object's instance, you have to use TransactionManager.GetObject() to open the database object.
    
    
    ' VBA:
    Dim oCurrentAlignment As AeccAlignment
    GetAlignmentAndOrigin(oRwyState, oCurrentAlignment, oOrigin)
    

In .NET:
    
    
    ' .NET:
    Dim currentAlignmentId As ObjectId
    Dim currentAlignment As Alignment
    Utilities.GetAlignmentAndOrigin(corridorState, currentAlignmentId, origin)
    ' ...
    Dim db As Database = Autodesk.AutoCAD.DatabaseServices.HostApplicationServices.WorkingDatabase
    Dim tm As Autodesk.AutoCAD.DatabaseServices.TransactionManager = db.TransactionManager
    currentAlignment = tm.GetObject(currentAlignmentId, OpenMode.ForRead, false, false)
