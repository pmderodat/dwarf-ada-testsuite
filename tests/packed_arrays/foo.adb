procedure Foo is
   type Item is range -32 .. 31;
   for Item'Size use 6;

   type Array_Type is array (Natural range <>) of Item;
   type Packed_Array_Type is array (Natural range <>) of Item;
   pragma Pack (Packed_Array_Type);

   AT_Long   : Array_Type :=
     (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15,
      16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31);
   PAT_Short : Packed_Array_Type := (-32, -1, 0, 1, 31);
   PAT_Long  : Packed_Array_Type :=
     (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15,
      16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31);

   type Bit_Field_Type is array (Natural range <>) of Boolean;
   pragma Pack (Bit_Field_Type);
   subtype Word_Bit_Field_Type is Bit_Field_Type (0 .. 15);

   WBF : Word_Bit_Field_Type := (True, False, True, True, others => False);

   subtype Half_Bit_Field_Type is Bit_Field_Type (0 .. 3);
   type Packed_Several_Packed_Type is array (Natural range <>)
                                      of Half_Bit_Field_Type;
   pragma Pack (Packed_Several_Packed_Type);

   HBT_False : Half_Bit_Field_Type := (others => False);
   HBT_True  : Half_Bit_Field_Type := (others => True);

   PSPT_Short : Packed_Several_Packed_Type := (HBT_True, HBT_False, HBT_True);
   PSPT_Long  : Packed_Several_Packed_Type (0 .. 31) :=
      (HBT_True,  HBT_False,
       HBT_True,  HBT_True,
       HBT_False, HBT_False,
       HBT_False, HBT_True,
       others => HBT_False);

   procedure Bar (A : Packed_Array_Type) is
   begin
      null;
   end Bar;

   procedure Bar (BF : Bit_Field_Type) is
   begin
      null;
   end Bar;

   procedure Bar (PSPT : Packed_Several_Packed_Type) is
   begin
      null;
   end Bar;

begin
   AT_Long (1) := AT_Long (4);
   PAT_Long (1) := AT_Long (1);
   PAT_Short (1) := AT_Long (1);
   Bar (PAT_Long);
   Bar (WBF);
   Bar (PSPT_Short);
   Bar (PSPT_Long);
end Foo;
