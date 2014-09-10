procedure Foo is
   type Record_Type (L, U : Integer) is record
      C : String (L .. U);
      case U is
         when 0 =>
            null;
         when 1 =>
            N : Natural;
         when others =>
            null;
      end case;
   end record;

   procedure Stop is
   begin
      null;
   end Stop;

   R : Record_Type (1, 1) := (1, 1, "b", 2);
begin
   Stop;
   R.N := R.N;
end Foo;
