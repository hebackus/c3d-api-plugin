<!-- Developer's Guide > API Developer's Guide >  .NET Core Developer's Guide > About Civil 3D .NET Core Development -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E6657034-71E5-4753-8AFD-139DC612B86D.htm -->

# About Civil 3D .NET Core Development

Starting with the 2025 release, Civil 3D now offers support for .NET 8. However, .NET framework-based plugins may encounter compatibility issues if they rely on features specific to the .NET framework. This section serves as a guide for both creating new Civil3D .NET 8 plugins and migrating existing .NET Framework-based plugin projects to .NET 8. It also provides debugging instructions within Civil 3D, outlines any known issues, and applies to subsequent .NET Core versions. 

Scope & Strategy

  * If your applications are [.NET Standard 2.x](<https://learn.microsoft.com/en-us/dotnet/standard/net-standard?tabs=net-standard-2-1>) assemblies, no migration is needed. 
  * If your application runs side by side and does not have runtime interoperability with Civil 3D/AutoCAD, you can continue using the legacy .NET framework as long as it remains supported by the [Microsoft .NET Framework - Microsoft Lifecycle](<https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-framework>). 
  * As per claims such as <https://github.com/dotnet/runtime/issues/68041>, .NET framework DLLs could continue to work within .NET Core runtime as long as they don't use any API exclusive to .NET Framework, However, you should conduct thorough testing on your own to ensure it functions properly within the .NET Core environment if you choose to stay with .NET framework. 
  * Otherwise, consider building .NET Standard 2.1 assemblies, which eliminates the need for further migration for a significant duration. Note that the .NET Standard is tailored for cross-platform compatibility, excluding Windows-specific features like WinForm, WPF, and C++/CLI that may be essential for your requirements. 
  * Or migrate to .NET 8, and address any [breaking changes](<https://learn.microsoft.com/en-us/dotnet/core/compatibility/8.0>) introduced in .NET 8. 
  * If migration to .NET 8 is not viable for any reason, you might explore an out-of-process solution. This involves hosting your .NET framework applications in a separate executable with the .NET framework runtime and communicating with Civil 3D through inter-process communication. Keep in mind that this approach may introduce performance overhead and additional interoperability complexities. 

Note: .NET LTS has a lifespan of only 3 years as indicated in [Microsoft .NET and .NET Core - Microsoft Lifecycle](<https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core>). Within the lifecycle of Civil 3D, we will continue upgrading to the next LTS versions, so you may need to consider upgrading accordingly. 

Development Environment

  * [Visual Studio 2022 V17.8 with .NET 8 SDK installed](<https://visualstudio.microsoft.com/downloads/>)
  * [Upgrade Assistant](<https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-install>)
