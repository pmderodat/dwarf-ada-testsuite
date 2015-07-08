procedure Foo is
   type Index_Type is range 100 .. 107;
   for Index_Type'Size use 4;

   type Small_Type is range 50 .. 57;

   type Array_Type is array (Index_Type range <>) of Natural;
   type Record_Type is record
      A, B : Small_Type;
   end record;
   for Record_Type use record
      A at 0 range 0 .. 2;
      B at 0 range 3 .. 5;
   end record;

   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;

   A : Array_Type :=
     (100 => 0, 101 => 1, 102 => 2, 103 => 3);
   I : Index_Type := 100;
   R : Record_Type := (A => 50, B => 57);

begin
   Discard (A);
   A (I) := 0;
   R.A := 50;
end Foo;
