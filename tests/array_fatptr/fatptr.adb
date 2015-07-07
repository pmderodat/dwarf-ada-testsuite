with Ada.Text_IO; use Ada.Text_IO;

procedure Fatptr is
   type Array_Type is array (Natural range <>) of Integer;
   type Array_Access is access Array_Type;

   procedure Put_Line (A : Array_Type);

   --------------
   -- Put_Line --
   --------------

   procedure Put_Line (A : Array_Type) is
      I : Natural := 0;
   begin
      Put ('(');
      for Item of A loop
         if I = 0 then
            Put (Natural'Image (A'First) & " => ");
         else
            Put (", ");
         end if;
         Put (Integer'Image (Item));
         I := I + 1;
      end loop;
      Put_Line (")");
   end Put_Line;

   A : Array_Type (1 .. 5) := (1, 2, 3, 4, 5);
   B : Array_Access := new Array_Type'(0 .. 6 => -1);
begin
   Put_Line (A);
   Put_Line (B.all);
end Fatptr;
