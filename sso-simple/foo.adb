with Ada.Unchecked_Conversion;

with Interfaces; use Interfaces;

with System;

procedure Foo is

   type Integer_Access is access all Integer;
   function Convert is new Ada.Unchecked_Conversion (Unsigned_64, Integer_Access);

   type R_Type is record
      I1, I2 : Integer;
      A      : Integer_Access;
   end record
   with Bit_Order            => System.High_Order_First,
        Scalar_Storage_Order => System.High_Order_First;

   type Embedded_Type is record
      I1, I2 : Integer;
      A      : Integer_Access;
   end record
   with Bit_Order            => System.Low_Order_First,
        Scalar_Storage_Order => System.Low_Order_First;

   --  for Embedded_Type use record
   --     I1 at 0 range 0 .. 31;
   --     I2 at 4 range 0 .. 31;
   --     A  at 8 range 0 .. 63;
   --  end record;

   type Composite_Type is record
      E : Embedded_Type;
      I : Integer;
   end record
   with Bit_Order            => System.High_Order_First,
        Scalar_Storage_Order => System.High_Order_First;

   procedure Process (R : R_Type) is
   begin
      null;
   end Process;

   procedure Process (E : Embedded_Type) is
   begin
      null;
   end Process;

   procedure Process (C : Composite_Type) is
   begin
      null;
   end Process;

   R : R_Type :=
     (I1 => 16#1011_1213#,
      I2 => 16#2021_2223#,
      A  => Convert (16#30313233_34353637#));
   E : Embedded_Type :=
     (I1 => R.I1,
      I2 => R.I2,
      A  => R.A);
   C : Composite_Type := (E => E, I => 16#40414243#);

begin
   Process (R);
   Process (E);
   Process (C);
   Process (C.E);
end Foo;
