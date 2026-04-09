<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Plot Your Drawing (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CE91C625-A278-4445-8219-3A2D880E6C22.htm -->

# Plot Your Drawing (.NET)

You can plot your drawing as it is viewed in Model space, or you can plot one of your prepared Paper space layouts. Plotting from Model space is often preferable when you want to view or verify your drawing prior to creating a Paper space layout. Once your model is ready, you can prepare and plot a Paper space layout. 

Note: The BACKGROUNDPLOT system variable controls if plotting occurs in the background or the foreground. Set BACKGROUNDPLOT to 0 to plot in the foreground. 

Plotting involves working with a number of different objects: PlotFactory, PlotEngine, PlotInfo, PlotSettings, PlotSettingsValidator, PlotInfoValidator, and PlotPageInfo. The PlotEngine object is responsible for generating a plot based on the information provided to it by a PlotInfo object. 

The PlotEngine object is used to generate the output of a layout. From the PlotEngine object, you can do the following: 

  * Plot to a file 
  * Plot to a plotter or printer 
  * Displays a preview of a layout
