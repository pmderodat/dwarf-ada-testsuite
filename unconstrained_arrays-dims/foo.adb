with Ada.Text_IO; use Ada.Text_IO;

procedure Foo is
   type Array_Type is array (Natural range <>, Natural range <>) of Integer;
   type Array_Access is access Array_Type;

   procedure Put_Line (A : Array_Type);

   --------------
   -- Put_Line --
   --------------

   procedure Put_Line (A : Array_Type) is
      I : Natural := 0;
   begin
      Put_Line ("(");
      for I in A'First (1) .. A'Last (1) loop
         Put ("  (");

         for J in A'First (2) .. A'Last (2) loop
            if J > A'First (2) then
               Put (", ");
            end if;
            Put (Integer'Image (A (I, J)));
         end loop;

         Put_Line ("),");
      end loop;
      Put_Line (")");
   end Put_Line;

   A : Array_Type (1 .. 3, 1 .. 2) := ((1, 2), (3, 4), (5, 6));
   B : Array_Access := new Array_Type'((1, 2, 3), (4, 5, 6));
begin
   Put_Line (A);
   Put_Line (B.all);
end Foo;
