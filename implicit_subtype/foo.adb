procedure Foo is
   type Record_Type (N : Positive) is record
      S : String (1 .. N);
   end record;

   procedure Discard (R : Record_Type) is
   begin
      null;
   end Discard;

   R1 : Record_Type := (1, "a");
   R2 : Record_Type := (2, "ab");
begin
   Discard (R1);
   Discard (R2);
   R1.S (1) := 'b';
end Foo;
