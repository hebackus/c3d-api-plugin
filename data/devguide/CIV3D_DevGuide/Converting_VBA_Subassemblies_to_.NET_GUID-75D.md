<!-- Developer's Guide > API Developer's Guide > Converting VBA Subassemblies to .NET -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-75D8F2C6-A7F7-492C-861B-1E29D3079FA1.htm -->

# Converting VBA Subassemblies to .NET

This chapter describes a process to convert existing custom subassemblies written in COM/VBA to .NET. 

Although VBA custom subassemblies are still supported in Autodesk Civil 3D 2026, VBA support is deprecated and will be discontinued in a future release. In addition, .NET subassemblies offer several advantages: they are easier to write and maintain, and most importantly, they offer significant performance improvements. On average, they perform about 50% faster than the equivalent code in VBA, and the performance increase can be even higher in complex drawings.

Once you have converted your custom subassemblies to .NET and imported them into the catalog file, you will need to update the dependent assemblies in your drawings, and re-build the corridors. See the last section in this Appendix for some sample code that replaces old VBA subassemblies with new .NET subassemblies.
