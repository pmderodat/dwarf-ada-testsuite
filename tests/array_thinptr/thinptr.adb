procedure Thinptr is
   type Array_Type is array (Natural range <>) of Integer;
   type Array_Access is access all Array_Type;
   for Array_Access'Size use Standard'Address_Size;

   procedure Discard (AA : Array_Access) is
   begin
      null;
   end Discard;

   B : Array_Access := new Array_Type'(0 .. 6 => -1);
begin
   Discard (B);
end Thinptr;
