<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Parcels > About Parcel Segments -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0775C68B-BAB5-4819-A582-A6C5C2551C77.htm -->

# About Parcel Segments

Each parcel segment is a collection of parcel segment elements, which are represented by objects derived from the AeccParcelSegmentElement base class. A segment element is an undivided part of a segment that can be used to create a parcel. When an element is intersected by another parcel segment, the element is split into two contiguous elements:
    
    
    Dim oSegments as AeccParcelSegments
    Set oSegments = oSite.ParcelSegments
     
    Dim oSegment1 as AeccParcelSegment
     
    ' Segment1 consists of 1 element, a line with endpoints
    ' at 500,100 to 600,100
    Set oSegment1 = oSegments.AddLine(500, 100, 600, 100)
    ' We can tell this by looking at the number of elements:
    Debug.Print oSegment1.Count ' returns 1
    ' If we cross the segment element with another segment,
    ' then the elements get split.
    Call oSegments.AddLine(550, 150, 550, 50)
     
    Debug.Print oSegment1.Count ' returns 2
    

The AeccParcelSegment.Item method returns each element as an object of type AeccParcelSegmentElement. This object has no Type property, so to determine what kind of element it represents you need to directly check the object type with the TypeOf operator:
    
    
    ' Loop through all elements of the parcel segment "oSegment"
     
    Dim i as Integer
    For i = 0 to oSegment.Count - 1
        Dim oElement As AeccParcelSegmentElement
        Set oElement = oSegment.Item(i)
     
        Debug.Print "Element " & i & ": " _
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
