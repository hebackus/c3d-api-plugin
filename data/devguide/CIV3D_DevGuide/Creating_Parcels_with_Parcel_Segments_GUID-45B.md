<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Parcels > Creating Parcels with Parcel Segments -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-45B5605C-E2EA-48DA-B2B1-3A9947C8B9C0.htm -->

# Creating Parcels with Parcel Segments

While a site contains a collection of parcels, this collection has no Add method. Instead, parcels are automatically generated from the parcel segments added to the AeccSite.ParcelSegments collection. A parcel segment is a 2-dimensional line, curve, or AutoCAD entity. Once a closed structure can be formed from the segments in the site, a parcel is automatically formed. Each additional parcel segment that forms new closed structures creates additional parcels. This may affect the shape of existing parcels - if an existing parcel is bisected by a new segment, the existing parcel is reduced in size and a new parcel is formed.
    
    
    Dim oSegments as AeccParcelSegments
    Set oSegments = oSite.ParcelSegments
     
    ' Parcel 1
    Call oSegments.AddLine(0, 0, 0, 200)
    Call oSegments.AddCurve(0, 200, -0.5, 200, 200)
    Call oSegments.AddLine(200, 200, 200, 0)
    Call oSegments.AddLine(200, 0, 0, 0)
     
    ' Parcel 2
    Call oSegments.AddCurve2(200, 200, 330, 240, 400, 200)
    Call oSegments.AddLine(400, 200, 400, 0)
     
    ' This will complete parcel 2, as well as form parcel 3.
    Dim oPolyline As AcadPolyline
    Dim dPoints(0 To 8) As Double
    dPoints(0) = 400: dPoints(1) = 0: dPoints(2) = 0
    dPoints(3) = 325: dPoints(4) = 25: dPoints(5) = 0
    dPoints(6) = 200: dPoints(7) = 0: dPoints(8) = 0
    Set oPolyline = oAeccDocument.Database.ModelSpace_
      .AddPolyline(dPoints)
    oPolyline.Closed = True
    ' Passing True as the second parameter deletes the
    ' polyline entity once the parcel segment has been created.
    Call oSegments.AddFromEntity(oPolyline, True)
