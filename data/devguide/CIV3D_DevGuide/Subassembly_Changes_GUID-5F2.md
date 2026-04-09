<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Subassembly Changes -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5F29809D-6BA5-4BBE-A063-9B65664D6EFD.htm -->

# Subassembly Changes

The “target mapping’ feature in Autodesk Civil 3D 2026 has changed, which affects how custom subassemblies are written. This feature now allows a subassembly to target object types in addition to alignments and profiles associated with the corridor that it requires to define its geometry. 

There are four changes to the way you write a custom subassembly: 

  1. New parameter types in ParamLogicalNameType
  2. New target collections in corridorState
  3. Targets are now objects 
  4. The CalcAlignmentOffsetToThisAlignment utility method is changed 

## New parameter types in ParamLogicalNameType

A subassembly can now target an offset target and elevation target (instead of an alignment and a profile), which are represented by new parameter types in ParamLogicalNameType. If you want to support the new target types in your subassemblies, you need to replace: 

  * ParamLogicalNameType.Alignment with 
    * ParamLogicalNameType.OffsetTarget — offset targets that are alignments, feature lines, survey figures and AutoCAD polylines OR 
    * ParamLogicalNameType.OffsetTargetPipe — offset targets that are pipe networks 
  * ParamLogicalNameType.Profile with 
    * ParamLogicalNameType.ElevationTarget — elevation targets that are profiles, feature lines, survey figures and AutoCAD 3D polylines OR 
    * ParamLogicalNameType.ElevationTargetPipe — elevation targets that are pipe networks 

## New target collections in corridorState

To get the offset and elevation target collections from the corridorState object, use ParamsOffsetTarget and ParamsElevationTarget instead of ParamsAlignment and ParamsProfile. All the offset targets (including network pipe offset targets) are in ParamsOffsetTarget, and all elevation targets (including network pipe elevation targets) are in ParamsElevationTarget. Here’s an example from the BasicLaneTransition.vb sample in the [Sample VB.NET Subassembly](<GUID-03ADCEE6-5B64-4BD2-96A2-79A9EC16F73D.htm>) section below: 
    
    
            Dim oParamsLong As ParamLongCollection
            oParamsLong = corridorState.ParamsLong
     
            Dim oParamsOffsetTarget As ParamOffsetTargetCollection
            oParamsOffsetTarget = corridorState.ParamsOffsetTarget
    

## Targets are now objects

Targets are now objects, instead of alignment or profile IDs. Now WidthOffsetTarget is defined for offset targets, and SlopeElevationTarget is defined for elevation targets, so you can declare targets as objects instead of IDs. Here’s an example from the BasicLaneTransition.vb sample in the [Sample VB.NET Subassembly](<GUID-03ADCEE6-5B64-4BD2-96A2-79A9EC16F73D.htm>) section below: 
    
    
            Dim offsetTarget As WidthOffsetTarget 'width or offset target
            offsetTarget = Nothing
            Dim elevationTarget As SlopeElevationTarget 'slope or elevation target
            elevationTarget = Nothing
    

### Changes to CalcAlignmentOffsetToThisAlignment() 

The CalcAlignmentOffsetToThisAlignment() utility method now calculate the offset from this alignment to the offset target. This method no longer returns the station value; it now returns the XY coordinate of the offset target at the point perpendicular to the alignment’s station. 

You can also now use the SlopeElevationTarget.GetElevation method to get an elevation on an elevation target directly, instead of using CalcAlignmentOffsetToThisAlignment(). Here’s an example from the BasicLaneTransition.vb sample in the [Sample VB.NET Subassembly](<GUID-03ADCEE6-5B64-4BD2-96A2-79A9EC16F73D.htm>) section below: 
    
    
                    'get elevation on elevationTarget
                    Try
                        dOffsetElev = elevationTarget.GetElevation(oCurrentAlignmentId, _
                           corridorState.CurrentStation, Utilities.GetSide(vSide))
                    Catch
                        Utilities.RecordWarning(corridorState, _
                           CorridorError.LogicalNameNotFound, _
                           "TargetHA", "BasicLaneTransition")
                        dOffsetElev = corridorState.CurrentElevation + vWidth * vSlope
                    End Try
