<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Designing Custom Subassemblies > Superelevation Behavior and Subassemblies -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-BA2BEB4B-464C-41C0-98A3-A9B092F3D9FE.htm -->

# Superelevation Behavior and Subassemblies

Make sure you consider differences in component behavior, such as when the roadway is in a normal crown condition or is in superelevation. Gutter and median subassemblies may also be designed to exhibit different behaviors in normal and superelevated sections. 

The superelevation properties of the corridor alignment define the lane and shoulder slopes at all stations on the roadway. However, the way these slopes are applied depends on a combination of how the subassemblies are manipulated in layout mode and the internal logic of the subassemblies. Different agencies have varying methodologies. The code behind the subassemblies makes it possible to adapt to just about any situation. 

Most importantly you need to determine where the superelevation pivot point is located, and how that point relates to the design profile grade line (PGL). Pivot point/PGL combinations that are commonly encountered include: 

  * Pivot point and PGL are both at the crown of road. 
  * Pivot point and PGL are at the inside edge-of-traveled-way on a divided road. 
  * Pivot point and PGL are at one edge-of-traveled-way on an undivided road. 
  * Pivot point is at the edge-of-traveled-way on the inside of the curve, while the PGL is at the centerline of the road. 
  * On a divided road with crowned roadways, the PGL is at the crown points, while the pivot point is at the inside edge-of-traveled-ways. 
  * On a divided road with uncrowned roadways, the PGL and pivot point is above the median at the centerline. 

Whatever the situation, the subassemblies must be designed so that they can be placed with the correct behavior. 

Sometimes the roadway components have special behavior in superelevated sections. Some examples of special superelevation behavior: 

  * **Broken Back Subbase.** Some agencies put a break point in the subbase layer on the high side of superelevation. The subbase parallels the finish grade up to a certain point, then extends at a downward slope until it intersects the shoulder or clear zone link. 
  * **Shoulder Breakover.** Usually a maximum slope difference, or breakover, must be maintained between the travel lane and the shoulder, or between the paved and unpaved shoulder links. 
  * **Curbs-and-Gutters.** Some agencies require that gutters on the high side of a superelevated road tip downward toward the low side, while others leave the gutters at their normal slope. 

Note:

When writing your custom subassembly, avoid writing code that makes AutoCAD calls and interrupts Autodesk Civil 3D subassembly operations during runtime. For example, avoid building selection sets. 

## Axis of Rotation Pivot Point Calculation Notes

This section explains the methods that must be called when creating subassemblies that use superelevation and support axis of rotation calculations. 

  * If one subassembly in an assembly is specified as a potential pivot, all subassemblies between it and the baseline that use superelevation must report their superelevation cross slope data to the corridor using the _Autodesk.CIvil.Runtime.CorridorState_ method: 
        
        Public Sub **SetAxisOfRotationInformation** (ByVal _isPotentialPivot_ As _Boolean_ , ByVal _superElevationSlope_ As _Double_ , ByVal _superElevationSlopeType_ As _Autodesk.Civil.Land.SuperelevationCrossSegmentType_ , ByVal _isReversedSlope_ As _Boolean_)

_superElevationSlope_ is the cross slope used in the subassembly. For axis of rotation to work correctly, it must be the value obtained from lane type _superElevationSlopeType_ in the superelevation table. If the value obtained from the table is adjusted in any way, axis of rotation will not work properly. 

_isReversedSlope_ set to True indicates that the cross slope applied is the negated value obtained from the superelevation table. 

  * The LaneSuperelevationAOR subassembly, which is provided in the Autodesk Civil 3D content, supports axis of rotation pivot points. If LaneSuperelevationAOR (or a custom subassembly that supports pivot points) is not contained in the assembly, the pivot type specified in the Calculate Superelevation wizard is ignored, and the Baseline Pivot Type is applied. A custom subassembly can support axis of rotation pivot points by passing in True for the _isPotentialPivot_ argument when calling SetAxisOfRotationInformation(). 
  * To determine the Centers pivots in a divided crowned roadway, the crown points specified in the subassemblies supporting pivots are used. To specify a crown point to be used in axis of rotation calculations when building the corridor, use the _Autodesk.Civil.Runtime.CorridorState_ method: 
        
        Public Sub **SetAxisOfRotationCrownPoint** (ByVal _nCrownPointIndex_ As _UInteger_)

To display the crown point in assembly layout mode, the subassembly property "SE AOR Crown Point For Layout" must be set with the index of the crown point. To set this property, call the following method in Utilities class: 
        
        Public Shared Sub **SetSEAORCrownPointForLayout** (ByVal _corridorState_ As _CorridorState_ , ByVal _nCrownPoint_ As _Integer_)

  * By default, the axis of rotation calculation assumes that the recorded cross slope is applied to the full width of the subassembly in its calculation. The starting offset will be the smallest offset in a subassembly drawn to the right, and the largest offset for a subassembly drawn to the left. If the subassembly is applying the cross slope to just a portion of the subassembly, record the starting and ending offsets of this range with the corridor using the _Autodesk.Civil.Runtime.CorridorState_ method: 
        
        Public Sub **SetAxisOfRotationSERange** (ByVal _dApplySE_StartOffset_ As _Double_ , ByVal _dApplySE_EndOffset_ As _Double_)

  * Only one set of axis of rotation information can be recorded per assembly. This means that the calculated delta Y value is the same no matter which point in the subassembly is used as the attachment point. Therefore, if a subassembly applies multiple cross slopes, or a single cross slope affects only certain point in the subassembly, only the pivot location will be correctly calculated and recorded to the corridor. 
  * If a subassembly uses superelevation, but does not record the superelevation cross slope data with the corridor, it should notify the corridor so that the corridor can issue a warning that axis of rotation results may be unexpected. To notify the corridor, call the following method in Utilities class: 
        
        Public Shared Sub **SetSEAORUnsupportedTag** (ByVal _corridorState_ As _CorridorState_)

If a subassembly conditionally supports axis of rotation, it may need to clear the unsupported flag. To clear the flag, call the following method in Utilities class: 
        
        Public Shared Sub **ClearSEAORUnsupportedTag** (ByVal _corridorState_ As _CorridorState_)
