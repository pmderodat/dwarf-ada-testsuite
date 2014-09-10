procedure Foo is
   type Index_Type is range 100 .. 107;
   for Index_Type'Size use 4;

   type Array_Type is array (Index_Type range <>) of Natural;

   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;

   A : Array_Type :=
     (100 => 0, 101 => 1, 102 => 2, 103 => 3);
   I : Index_Type := 100;

begin
   Discard (A);
   A (I) := 0;
end Foo;
