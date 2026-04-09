<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Root Objects > Accessing Extended Properties -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8B59968F-71AC-4A91-80B7-5F61F7FBFD6A.htm -->

# Accessing Extended Properties

Survey root objects can have extended properties associated with them. LandXML extended properties are used to import and export Survey LandXML attributes or collections of elements. For example, in the LandXML schema, a CgPoint element (a SurveyPoint) within a CgPoints collection (a SurveyPointGroup), may contain a DTMAttribute where its enumeration value can be used to aid the user in determining whether the point should be included in a surface definition. User-defined extended properties can be used to define additional attributes beyond those defined by the LandXML schema. For an example of standard LandXML extended properties, see the C:\Documents and Settings\All Users\Application Data\Autodesk\C3D2012\enu\Survey\LandXML - Standard.sdx_deffile. 

The AeccSurveyFigure, AeccSurveyNetwork, AeccSurveyPoint, and AeccSurveyProject objects each have a LandXMLXPropertiesRoot property, which gives you access to the AeccSurveyLandXMLXPropertiesRoot for that object. Those objects also each have a UserDefinedXProperties object, which gives you access to the AeccSurveyUserDefinedXProperties for that object.
