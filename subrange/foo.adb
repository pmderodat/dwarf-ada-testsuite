procedure Foo is
   type Range_Type is (One, Two, Three);

   type Array_Type is array (Range_Type range One .. Two) of Integer;
   type Array2_Type is array (Range_Type range Two .. Three) of Integer;

   subtype Subrange_Type is Range_Type range Two .. Three;
   type Array3_Type is array (Subrange_Type) of Integer;

   V : Subrange_Type := Two;
   A : Array_Type := (1, 2);
   A2 : Array2_Type := (2, 3);
   A3 : Array3_Type := (3, 4);
begin
   V := Three;
   A (Two) := A2 (Two);
   A2 (Two) := A3 (Two);
   A3 (Two) := A (Two);
end Foo;
