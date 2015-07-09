procedure Foo is
   type FP1_Type is delta 0.1 range -1.0 .. +1.0; --  Ordinary
   type FP2_Type is delta 0.01 digits 14;         --  Decimal

   type FP3_Type is delta 0.1 range 0.0 .. 1.0
      with Small => 0.1/3.0;

   Delta4 : constant := 0.000_000_000_000_000_000_1;
   type FP4_Type is delta Delta4 range 0.0 .. Delta4 * 10
      with Small => Delta4 / 3.0;

   procedure Discard (V : FP1_Type) is
   begin
      null;
   end Discard;

   procedure Discard (V : FP2_Type) is
   begin
      null;
   end Discard;

   procedure Discard (V : FP3_Type) is
   begin
      null;
   end Discard;

   procedure Discard (V : FP4_Type) is
   begin
      null;
   end Discard;

   A1 : array (Positive range <>) of FP1_Type :=
     (-1.0, 0.1, 0.3);

   A2 : array (Positive range <>) of FP2_Type :=
     (+0.00, -0.01, +10.03);

   A3 : array (Positive range <>) of FP3_Type :=
     (+0.0, +0.1, +0.2, +1.0);

   A4 : array (Positive range <>) of FP4_Type :=
     (0.0, Delta4, 2 * Delta4);

begin
   Discard (A1 (1));
   Discard (A2 (1));
   Discard (A3 (1));
   Discard (A4 (1));
end Foo;
