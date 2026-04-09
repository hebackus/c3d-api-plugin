<!-- Developer's Guide > API Developer's Guide >  .NET Core Developer's Guide > Migrate Existing Projects > To Migrate C++/CLI Projects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C6900644-A4E4-4EC3-AF6F-375C4EF58138.htm -->

# To Migrate C++/CLI Projects

Reference documents:

  * [Porting C++/CLI Projects to .NET Core](<https://docs.microsoft.com/en-us/dotnet/core/porting/cpp-cli>)
  * [Porting a C++/CLI Project to .NET Core](<https://devblogs.microsoft.com/cppblog/porting-a-c-cli-project-to-net-core/>)

To modify a .vcxproj file

  1. Add <TargetFramework>net8.0-windows</TargetFramework>. 

Note: For TargetFramework, use net8.0 if there is not a specific Windows dependency. 

  2. Change <CLRSupport>true</CLRSupport> to <CLRSupport>NetCore</CLRSupport> for Release and Debug. 
  3. Remove all .NET Framework references (such as System, System.Core, and System.Data). 
  4. Then, rebuild only the project in Visual Studio.
