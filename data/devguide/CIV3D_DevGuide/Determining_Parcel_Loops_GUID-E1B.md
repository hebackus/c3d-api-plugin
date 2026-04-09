<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Parcels > Determining Parcel Loops -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E1BE9771-F2CE-48AA-B08F-4AB046F63EFC.htm -->

# Determining Parcel Loops

You can determine which parcel segment elements make up a parcel by using the AeccParcel.ParcelLoops collection. This collection stores objects of type AeccParcelSegmentElement. Each parcel segment element contains a reference to the parent segment, so you can also determine which segments are used to create a parcel.
    
    
    ' Loop through all elements used to make parcel "oParcel"
     
    Dim i as Integer
    For i = 0 to oParcel.ParcelLoops.Count - 1
        Dim oElement As AeccParcelSegmentElement
        Set oElement = oParcel.ParcelLoops.Item(i)
     
        Debug.Print "Element " & i _
          & " of segment " & oElement.ParcelSegment.Name & ": " _
          & oElement.StartX & "," & oElement.StartY & " to " _
          & oElement.EndX & ", " & oElement.EndY
     
        If (TypeOf oElement Is AeccParcelSegmentLine) Then
            Dim oSegmentLine As AeccParcelSegmentLine
            Set oSegmentLine = oElement
            Debug.Print " is a line. "
        ElseIf (TypeOf oElement Is AeccParcelSegmentCurve) Then
            Dim oSegmentCurve As AeccParcelSegmentCurve
            Set oSegmentCurve = oElement
            Debug.Print " is a curve with a radius of:" _
              & oSegmentCurve.Radius
        End If
    Next i
