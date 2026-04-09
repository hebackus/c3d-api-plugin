<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Dimension in Model Space and Paper Space (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8A307344-383A-4141-912C-92A7B0C4B5E6.htm -->

# Dimension in Model Space and Paper Space (.NET)

You can draw dimensions in both Model space and Paper space. However, if the geometry you are dimensioning is in Model space, it is best to draw dimensions in Model space because AutoCAD places the definition points in the space where the geometry is drawn. 

If you draw a dimension in Paper space that describes geometry in your model, the Paper space dimension does not change when you use editing commands or change the magnification of the display in the Model space viewport. The location of the Paper space dimensions also stays the same when you change a view from Paper space to Model space. 

If you are dimensioning in Paper space and the global scale factor for linear dimensioning (the DIMLFAC system variable) is set at less than 0, the distance measured is multiplied by the absolute value of DIMLFAC. If you are dimensioning in Model space, the value of 1.0 is used even if DIMLFAC is less than 0. AutoCAD computes a value for DIMLFAC if you change the variable at the Dim prompt and select the Viewport option. AutoCAD calculates the scaling of Model space to Paper space and assigns the negative of this value to DIMLFAC.
