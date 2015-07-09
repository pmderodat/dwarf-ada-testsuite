procedure Foo is
   type Array_Type is array (Natural range <>, Natural range <>) of Integer;
   type Array_Access is access Array_Type;

   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;

   A : Array_Type (1 .. 3, 1 .. 2) := ((1, 2), (3, 4), (5, 6));
   B : Array_Access := new Array_Type'((1, 2, 3), (4, 5, 6));
begin
   Discard (A);
   Discard (B.all);
end Foo;
