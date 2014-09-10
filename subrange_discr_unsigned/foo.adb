with Ada.Text_IO; use Ada.Text_IO;
with Interfaces;  use Interfaces;

procedure Foo is
   subtype Bound_Type is Unsigned_64;
   type Array_Type is array (Bound_Type range <>) of Integer;
   type Record_Type (Low, High : Bound_Type) is limited record
      A : Array_Type (Low .. High);
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
      Put_Line ("Low =" & Bound_Type'Image (R.Low));
      Put_Line ("High =" & Bound_Type'Image (R.High));
      Put ("A = ");
      Put_Line (R.A);
   end Put_Line;

   Low : constant Bound_Type := 16#ffff_ffff_ffff_fffc#;
   High : constant Bound_Type := 16#ffff_ffff_ffff_ffff#;
   R : Record_Type :=
     (Low  => Low,
      High => High,
      A    => (2, 3, 4, 5));
begin
   R.A (R.A'First) := 1;
   Put_Line (Integer'Image (R.A (R.A'First + 1)));
   Put_Line (Bound_Type'Image (R.A'Last));
   Put_Line (R);
end Foo;
