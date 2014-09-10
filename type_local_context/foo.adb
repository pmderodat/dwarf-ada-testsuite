procedure Foo is
   type Record_Type is record
      I : Integer;
   end record;

   procedure Bar (R : Record_Type) is
   begin
      null;
   end Bar;

   R : Record_Type := (I => 1);

begin
   Bar (R);
end Foo;
