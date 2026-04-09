<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Parcels > Parcel Style and Parcel Segment Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8DC2E6AE-D1C8-4D67-9535-BCFEB730260A.htm -->

# Parcel Style and Parcel Segment Style

The collection of all parcel styles is held in the AeccDocument.ParcelStyles collection. The parcel style controls how a parcel and the parcel segments are displayed. Among the features is an option to only fill the area close to a parcel’s borders. A parcel style can be assigned to a parcel through the AeccParcel.Style property.

This sample creates a parcel style, sets the style properties, and assigns the style to the parcel object “oParcel”:
    
    
    Dim oParcelStyles As AeccParcelStyles
    Set oParcelStyles = oDocument.ParcelStyles
    Dim oParcelStyle As AeccParcelStyle
    Set oParcelStyle = oParcelStyles.Add("Sample Style")
    oParcelStyle.ObservePatternFillDistance = True
    oParcelStyle.PatternFillDistance = 20
    oParcelStyle.SegmentsDisplayStylePlan.color = 20 ' red-orange
    oParcelStyle.AreaFillDisplayStylePlan.color = 20
    oParcelStyle.AreaFillDisplayStylePlan.Visible = True
    oParcelStyle.AreaFillDisplayStylePlan.Lineweight = 20
    oParcelStyle.AreaFillHatchDisplayStylePlan.UseAngleOfObject = True
    oParcelStyle.AreaFillHatchDisplayStylePlan.ScaleFactor = 3.8
    oParcelStyle.AreaFillHatchDisplayStylePlan.Spacing = 1.5
    oParcelStyle.AreaFillHatchDisplayStylePlan.Pattern = "AR-SAND"
    oParcelStyle.AreaFillHatchDisplayStylePlan.HatchType = aeccHatchPreDefined
     
    ' Assign the "Sample Style" style to a single parcel.
    oParcel.Style = oParcelStyle.Name
    

The style of individual parcel segments depends on the style of the parent parcel, but segments may be shared by different parcels. This conflict is decided by the AeccParcels.Properties.SegmentDisplayOrder property, which is a collection of all parcel styles currently in use. These styles are arranged according to priority level. When two parcels with different styles share a segment, the segment is displayed with the higher priority style. Among these styles is the global site parcel style, set through the AeccParcels.Properties.SiteParcelStyle property. The site parcel style defines the outside boundary style of parcels within the site, given a high enough priority. 

This sample displays the current order of parcel styles in the site and then modifies the order:
    
    
    ' List all styles used by parcels in this site with their
    ' priority 
    Dim oSegmentDisplayOrder As AeccSegmentDisplayOrder
    Set oSegmentDisplayOrder = _
      oSite.Parcels.Properties.SegmentDisplayOrder
     
    Debug.Print "Number styles used:"; oSegmentDisplayOrder.Count
    Debug.Print "Priority of each style for affecting segments:"
    Dim i as Integer
    For i = 0 To oSegmentDisplayOrder.Count - 1
        Debug.Print i; " & oSegmentDisplayOrder.Item(i).Name
    Next i
     
    ' Set the style with the highest priority to the lowest
    ' priority.
    Dim lLowestPosition as Long
    lLowestPosition = oSegmentDisplayOrder.Count - 1
    oSegmentDisplayOrder.SetPriority 0, lLowestPosition
