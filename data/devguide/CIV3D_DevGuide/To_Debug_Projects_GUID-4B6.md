<!-- Developer's Guide > API Developer's Guide >  .NET Core Developer's Guide > To Debug Projects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4B65B45B-5C51-4637-ACC5-6E8067C863E6.htm -->

# To Debug Projects

  1. In Visual Studio, select Debug  Attach to Process (or press `Ctrl+Alt+P`) to open the Attach to Process dialog box. 
  2. Select the code types. Choose both if you want to do the mixed debugging. 

     * Managed(.NET Core, .NET 5+) for .NET Core codes debugging 
     * Native - C/C++ for native code debugging 

To facilitate your debugging

  1. Switch your configuration to Debug. 

  2. Add necessary calls in your class so that you can understand the state of your program. 
         
         Debug.WriteLine("Just a test");
