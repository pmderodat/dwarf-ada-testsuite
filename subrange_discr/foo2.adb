with Ada.Text_IO; use Ada.Text_IO;

procedure Foo2 is
   type Array_Type is array (Natural range <>) of Integer;
   type Record_Type (Length : Natural) is record
      A : Array_Type (1 .. Length);
   end record;

   procedure Put_Line (A : Array_Type) is
      First : Boolean := True;
   begin
      Put ("(");
      for Item of A loop
         if not First then
            Put (", ");
         end if;
         Put (Natural'Image (Item));
         First := False;
      end loop;
      Put_Line (")");
   end Put_Line;

   procedure Put_Line (R : Record_Type) is
   begin
      Put_Line ("Length =" & Natural'Image (R.Length));
      Put ("A = ");
      Put_Line (R.A);
   end Put_Line;

   function Get return Record_Type is
   begin
     return
        (Length => 2,
         A      => (0, 2));
   end Get;

   R : Record_Type := Get;

begin
   R.A (1) := 1;
   Put_Line (R);
end Foo2;
