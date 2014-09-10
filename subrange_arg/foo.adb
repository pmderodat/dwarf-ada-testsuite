procedure Foo is

   function Range_Count (L, U : Integer) return Natural
   is
      type Array_Type is array (L .. U) of Natural;

      A : Array_Type := (others => 1);
      Result : Natural := 0;
   begin
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
