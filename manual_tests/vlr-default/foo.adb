procedure Foo is
   subtype Small_Type is Integer range 0 .. 10;
   type Record_Type (I : Small_Type := 0) is record
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
   Discard (A1 (2));
end Foo;
