procedure Foo is
   type Array_Type is array (Natural range <>) of Integer;
   type Record_Type (Length1, Length2 : Natural) is record
      A1 : Array_Type (1 .. Length1);
      A2 : Array_Type (Length1 .. Length2);
   end record;

   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;

   procedure Discard (R : Record_Type) is
   begin
      null;
   end Discard;

   R : Record_Type :=
     (Length1 => 2,
      Length2 => 5,
      A1      => (0, 2),
      A2      => (2, 3, 4, 5));
begin
   R.A1 (1) := 1;
   Discard (R.A1);
   Discard (R.A2);
   Discard (R);
end Foo;
