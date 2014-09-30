with Ada.Unchecked_Conversion;

package body Dwarf_Handling is
   function Read_String (Addr : Address) return String
   is
      function C_Strlen (Addr : Address) return Integer;
      pragma Import (C, C_Strlen, "strlen");
      Len : Integer;

      subtype Fat_String is String (Positive);
      type Fat_String_Acc is access Fat_String;
      function To_Fat_String is new Ada.Unchecked_Conversion
        (Address, Fat_String_Acc);
      Str : constant Fat_String_Acc := To_Fat_String (Addr);
   begin
      if Addr = Null_Address then
         return "";
      end if;
      Len := C_Strlen (Addr);
      return Str (1 .. Len);
   end Read_String;
end Dwarf_Handling;
