<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with TIN Surfaces > Extracting Contours from a TIN Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-36E43E94-6D1C-4636-8A8C-478AC51F7256.htm -->

# Extracting Contours from a TIN Surface

You can extract a contour (or contours) from a surface in a given elevation range as AutoCAD entities. This example extracts the contours between 90 and 95, and prints out the entity type for each one.

Note:

The contours that you wish to extract must be visible in the drawing for this example to work.
    
    
    ...
    Dim z As Double
    Dim objSurf As AeccSurface
    Set objSurf = g_oAeccDoc.Surfaces(0)
    Dim varObjects As Variant
    Dim objEnt As AcadEntity
    Dim iCtr As Integer, iLow As Integer, iHigh As Integer
    varObjects = objSurf.ExtractContour(aeccDisplayOrientationPlan, aeccSFMajorContours, 90, 95)
    iLow = LBound(varObjects)
    iHigh = UBound(varObjects)
    For iCtr = iLow To iHigh
       Set objEnt = varObjects(iCtr)
       Debug.Print TypeName(objEnt)
    Next iCtr
