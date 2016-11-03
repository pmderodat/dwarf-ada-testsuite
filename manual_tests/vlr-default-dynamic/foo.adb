procedure Foo is

   procedure Nested (L, U : Integer) is
      subtype Small_Type is Integer range L .. U;
      type Record_Type (I : Small_Type := L) is record
         S : String (1 .. I);
      end record;
      type Array_Type is array (Integer range <>) of Record_Type;

      A1 : Array_Type :=
        (1 => (I => 0, S => <>),
         2 => (I => 1, S => "A"),
         3 => (I => 2, S => "AB"));

      procedure Discard (R : Record_Type) is
      begin
         null;
      end Discard;

   begin
      Discard (A1 (1));
   end;

begin
   Nested (0, 10);
   Nested (-10, 10);
end Foo;
