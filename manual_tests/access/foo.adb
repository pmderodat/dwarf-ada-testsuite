procedure Foo is
   subtype Int is Integer;
   type Record_Type is null record;
   type UArray_Type is array (Natural range <>) of Integer;
   subtype CArray_Type is UArray_Type (1 .. 10);

   type Integer_Access is access all Integer;
   type Record_Access is access all Record_Type;
   type UArray_Access is access all UArray_Type;
   type CArray_Access is access all CArray_Type;

   procedure Discard (A : UArray_Type) is
   begin
      null;
   end Discard;

   I : Int := 0;
   P_I : Integer_Access := null;
   P_R : Record_Access := null;
   P_UA : UArray_Access := new UArray_Type'(1 .. 5 => 0);
   P_CA : CArray_Access := null;
begin
   Discard (P_UA.all);
end Foo;
