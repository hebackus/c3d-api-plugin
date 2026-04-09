<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Single-Line Text (.NET) > Set Text Height (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9713948C-0EC9-4916-B231-5D17495FC242.htm -->

# Set Text Height (.NET)

Text height determines the size in drawing units of the letters in the font you are using. The value usually represents the size of the uppercase letters, with the exception of TrueType fonts. 

For TrueType fonts, the value specified for text height might not represent the height of uppercase letters. The height specified represents the height of a capital letter plus an accent area reserved for accent marks and other marks used in non-English languages. The relative portion of areas assigned to capital letters and accent characters is determined by the font designer at the time the font is designed, and, consequently, will vary from font to font. 

In addition to the height of a capital letter and the ascent area that make up the height specified by the user, TrueType fonts have a descent area for portions of characters that extend below the text insertion line. Examples of such characters are y, j, p, g, and q. 

You specify the text height using the TextSize property of the text style or the Height property of a text object. This property accepts positive numbers only.
