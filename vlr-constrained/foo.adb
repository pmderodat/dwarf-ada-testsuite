procedure Foo is
   type Record_Type (N : Natural) is record
      S : String (1 .. N);
   end record;

   subtype Record_Constrained_Type is Record_Type (8);
   type Record_Array_Type is
      array (Integer range <>) of Record_Constrained_Type;

   procedure Discard (R : Record_Type) is
   begin
      null;
   end Discard;

   R1 : Record_Type := (N => 1, S => "A");
   A1 : Record_Array_Type :=
     (1 => (N => 8, S => "ABCDEFGH"),
      2 => (N => 8, S => "01234567"));
begin
   Discard (R1);
   Discard (A1 (2));
end Foo;
