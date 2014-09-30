procedure Foo is
   type Array_Type is array (Natural range <>) of Integer;
   type Record_Type (L1, L2 : Natural) is record
      I1 : Integer;
      A1 : Array_Type (1 .. L1);
      I2 : Integer;
      A2 : Array_Type (1 .. L2);
      I3 : Integer;
   end record;

   function Get (L1, L2 : Natural) return Record_Type is
      Result : Record_Type (L1, L2);
   begin
      Result.I1 := 1;
      for I in Result.A1'Range loop
         Result.A1 (I) := I;
      end loop;
      Result.I2 := 2;
      for I in Result.A2'Range loop
         Result.A2 (I) := I;
      end loop;
      Result.I3 := 3;
      return Result;
   end Get;

   R1 : Record_Type := Get (0, 0);
   R2 : Record_Type := Get (1, 0);
   R3 : Record_Type := Get (0, 1);
   R4 : Record_Type := Get (2, 2);

   procedure Process (R : Record_Type) is
   begin
      null;
   end Process;

begin
   Process (R1);
   Process (R2);
   Process (R3);
   Process (R4);
end Foo;
