procedure Foo is
   type R2_Type is record
      B : Boolean;
   end record;

   type R1_Type is record
      I  : Integer;
      R2 : R2_Type;
   end record;

   R1 : R1_Type;

begin
   R1.I := 0;
end Foo;
