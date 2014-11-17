procedure Foo is
   type Array_Type is array (Natural range <>) of Integer;
   type Record_Type (L1, L2 : Natural) is record
      I1 : Integer;
      A1 : Array_Type (1 .. L1);
      I2 : Integer;
      A2 : Array_Type (1 .. L2);
      I3 : Integer;
   end record;

   procedure Process (R : Record_Type) is
   begin
      null;
   end Process;

   R00 : Record_Type :=
     (L1 => 0, L2 => 0,
      I1 => 1, A1 => (others => 10),
      I2 => 2, A2 => (others => 20),
      I3 => 3);
   R01 : Record_Type :=
     (L1 => 0, L2 => 1,
      I1 => 1, A1 => (others => 10),
      I2 => 2, A2 => (others => 20),
      I3 => 3);
   R10 : Record_Type :=
     (L1 => 1, L2 => 0,
      I1 => 1, A1 => (others => 10),
      I2 => 2, A2 => (others => 20),
      I3 => 3);
   R22 : Record_Type :=
     (L1 => 2, L2 => 2,
      I1 => 1, A1 => (others => 10),
      I2 => 2, A2 => (others => 20),
      I3 => 3);

begin
   Process (R00);
   Process (R01);
   Process (R10);
   Process (R22);
end Foo;
