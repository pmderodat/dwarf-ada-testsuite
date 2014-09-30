procedure Foo is
   type Item is range -32 .. 31;
   for Item'Size use 6;

   type Array_Type is array (Natural range <>) of Item;
   type Packed_Array_Type is array (Natural range <>) of Item;
   pragma Pack (Packed_Array_Type);

   type Bit_Field_Type is array (Natural range <>) of Boolean;
   pragma Pack (Bit_Field_Type);
   subtype Word_Bit_Field_Type is Bit_Field_Type (0 .. 15);

   A_Short : Packed_Array_Type := (-32, -1, 0, 1, 31);
   A_Long  : Packed_Array_Type :=
     (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15,
      16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31);
   A_Long2 : Array_Type :=
     (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15,
      16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31);

   WBF : Word_Bit_Field_Type := (True, False, True, True, others => False);

   procedure Bar (A : Packed_Array_Type) is
   begin
      null;
   end Bar;

   procedure Bar (BF : Bit_Field_Type) is
   begin
      null;
   end Bar;

begin
   A_Long2 (1) := A_Long2 (4);
   A_Long (1) := A_Long2 (1);
   A_Short (1) := A_Long2 (1);
   Bar (A_Long);
   Bar (WBF);
end Foo;
