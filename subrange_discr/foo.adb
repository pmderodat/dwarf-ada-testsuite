with Ada.Text_IO; use Ada.Text_IO;

procedure Foo is
   type Array_Type is array (Natural range <>) of Integer;
   type Record_Type (Length1, Length2 : Natural) is record
      A1 : Array_Type (1 .. Length1);
      A2 : Array_Type (Length1 .. Length2);
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
      Put_Line ("Length1 =" & Natural'Image (R.Length1));
      Put_Line ("Length2 =" & Natural'Image (R.Length2));

      Put ("A1 = ");
      Put_Line (R.A1);

      Put ("A2 = ");
      Put_Line (R.A2);
   end Put_Line;

   R : Record_Type :=
     (Length1 => 2,
      Length2 => 5,
      A1      => (0, 2),
      A2      => (2, 3, 4, 5));
begin
   R.A1 (1) := 1;
   Put_Line (Integer'Image (R.A1 (2)));
   Put_Line (Natural'Image (R.A1'Last));
   Put_Line (R);
end Foo;
