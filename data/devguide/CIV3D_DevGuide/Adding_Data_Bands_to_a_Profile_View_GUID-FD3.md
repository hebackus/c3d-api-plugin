<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Using Data Bands > Adding Data Bands to a Profile View -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FD318BAB-3A68-4885-B40B-96F934CCF03A.htm -->

# Adding Data Bands to a Profile View

Every profile view contains a collection of bands in its AeccProfileView.BandSet property, an object of type AeccProfileViewBandSet. When a profile view is first created, all band styles from the AeccProfileViewBandStyleSet parameter are added to this collection. Individual band styles can be added to a section view through the AeccProfileViewBandSet collection using its Add or Insert methods. Both of these methods take an AeccProfileDataBandStyle style, a parent alignment, and two AeccProfile objects, allowing comparison between profiles.

Tip:

If you only want to display information from a single profile in the band, pass the same profile object to both parameters.

The order of bands in the band set is also the order in which the bands are displayed. AeccProfileViewBandSet.Add places the new band at the bottom of the list while AeccProfileViewBandSet.Insert places the new band at the specified index.

Tip:

You can swap the location of two bands with the AeccProfileViewBandSet.Swap method.

This sample adds a data band to a profile view that describes the single profile “oProfile” based on the alignment “oAlignment”:
    
    
    Dim oProfileViewBandSetItem As AeccProfileViewBandSetItem
    Set oProfileViewBandSetItem = oProfileView.BandSet.Add( _
      oBandStyle, _
      oAlignment, _
      oProfile, _
      oProfile)
      
    ' Now oProfileView has another data band.
