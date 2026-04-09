<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Viewports (.NET) > Scale Views Relative to Paper Space (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4A177301-1624-45F5-97E9-8832E484B0FB.htm -->

# Scale Views Relative to Paper Space (.NET)

Before you plot, you can establish the scale factor for the view in each viewport. Scaling views relative to paper space establishes a consistent scale for each displayed view. For example, the following illustration shows a Paper space view with several viewports—each set to different scales and views. 

When you work in Paper space, the scale factor represents a ratio between the size of the plotted drawing and the actual size of the model displayed in the viewports. To derive this scale, divide paper space units by Model space units. For a quarter-scale drawing, for example, you specify a scale factor of one Paper space unit to four Model space units (1:4). 

The StandardScale and CustomScale properties are used to specify the scale for a viewport. The StandardScale property accepts a value based on the StandardScaleType enum; whereas the CustomScale property accepts a real number which represents the ratio of units between Model and Paper space. For example, the real value equal to 1:4 is 0.25. 

The following illustrations show the view of the model at a scale of 1:1, and then the same model view show at scales of 2:1 and 1:2. A scale of 2:1 increases the view of the model to twice the size of the paper space units; while a scale of 1:2 displays the model at half its actual size.
