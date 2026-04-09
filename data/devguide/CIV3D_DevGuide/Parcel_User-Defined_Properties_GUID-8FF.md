<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sites and Parcels in COM > Parcels > Parcel User-Defined Properties -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8FF68D08-AE46-49EF-8357-FB4586E89CE4.htm -->

# Parcel User-Defined Properties

Parcel objects can have user-defined properties associated with them, and the properties can be organized into user-defined classifications, or are put into an “Unclassified” classification. You can create new classifications and user-defined properties via the API, though you can’t access the values of existing user-defined properties attached to parcels. 

This sample creates a new user-defined property classification for parcels called “Example”, and then adds a new user-defined property with upper and lower bounds and a default value: 
    
    
    Dim oApp As AcadApplication
    Set oApp = ThisDrawing.Application
    ' NOTE - Always specify the version number.
    Const sAppName = "AeccXUiLand.AeccApplication.6.0"
    Set g_vCivilApp = oApp.GetInterfaceObject(sAppName)
    Set g_oDocument = g_vCivilApp.ActiveDocument
    Set g_oAeccDb = g_oDocument.Database
    Dim oUDPClass As AeccUserDefinedPropertyClassification
    Dim oUDPProp As AeccUserDefinedProperty
    'Create a user-defined parcel property classification
    Set oUDPClass = g_oAeccDb.ParcelUserDefinedPropertyClassifications.Add("Example")
    ' Add a Property to our new classification An integer using upper 
    ' and lower bound limits of 10 and 20 with a default value of 15
    Set oUDPProp = oUDPClass.UserDefinedProperties.Add("Extra Data", _
       "Some Extra Data", aeccUDPPropertyFieldTypeInteger, True, False, 10, True, _
       False, 20, True, 15, Null)
