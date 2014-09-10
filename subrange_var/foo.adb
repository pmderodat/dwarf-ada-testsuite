procedure Foo is

   function Range_Count (L, U : Integer) return Natural
   is
      Low : Integer := L;
      Up  : Integer := U;
      type Array_Type is array (Low .. Up) of Natural;

      A : Array_Type := (others => 1);
      Result : Natural := 0;
   begin
      Low := 0;
      Up := 0;
      for I of A loop
         Result := Result + I;
      end loop;
      return Result;
   end Range_Count;

   R1 : constant Natural := Range_Count (10, 4);
   R2 : constant Natural := R1 + Range_Count (0, 5);
   R3 : constant Natural := R1 + Range_Count (5, 5);
begin
   null;
end Foo;
