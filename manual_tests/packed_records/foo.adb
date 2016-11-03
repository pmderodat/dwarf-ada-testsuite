with Ada.Text_IO; use Ada.Text_IO;

procedure Foo is
   type Item is range -32 .. 31;
   for Item'Size use 6;

   type Record_Type is record
      B1 : Boolean;
      I1 : Item;
      N1 : Natural;
      B2 : Boolean;
   end record;
   pragma Pack (Record_Type);

   type Array_Type is array (Natural range <>) of Record_Type;
   pragma Pack (Array_Type);

   procedure Put_Line (R : in out Record_Type) is
   begin
      Put ("(");
      Put (Boolean'Image (R.B1));
      Put (", ");
      Put (Item'Image (R.I1));
      Put (", ");
      Put (Natural'Image (R.N1));
      Put_Line (")");
   end Put_Line;

   procedure Put_Line (A : in out Array_Type) is
   begin
      for R of A loop
         Put_Line (R);
      end loop;
   end Put_Line;

   R1 : Record_Type := (True, 0, Natural'Last, False);
   R2 : Record_Type := (False, Item'First, 0, False);
   A : Array_Type := (R1, R2);
begin
   Put_Line (R1);
   Put_Line (R2);
   Put_Line (" -- ");
   Put_Line (A);
end Foo;
