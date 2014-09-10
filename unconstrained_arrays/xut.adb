with Ada.Text_IO; use Ada.Text_IO;

procedure XUT is
   type Array_Type is array (Natural range <>) of Integer;
   type Array_Access is access all Array_Type;
   for Array_Access'Size use 64;

   procedure Put_Line (AA : Array_Access);
   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;

   --------------
   -- Put_Line --
   --------------

   procedure Put_Line (AA : Array_Access) is
      B : constant Natural := AA.all'First;
      A : Array_Type renames AA.all;
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

   B : Array_Access := new Array_Type'(0 .. 6 => -1);
begin
   Discard (B.all);
   Put_Line (B);
end XUT;
