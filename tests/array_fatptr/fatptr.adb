procedure Fatptr is
   type Array_Type is array (Natural range <>) of Integer;
   type Array_Access is access Array_Type;

   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;

   A : Array_Type (1 .. 5) := (1, 2, 3, 4, 5);
   B : Array_Access := new Array_Type'(0 .. 6 => -1);
begin
   Discard (A);
   Discard (B.all);
end Fatptr;
