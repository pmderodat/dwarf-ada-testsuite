with Ada.Text_IO; use Ada.Text_IO;

procedure Foo is
   type R1 is record
      I : Integer;
   end record;

   type R2 is record
      N : Natural;
      R : R1;
   end record;

   R : R2 :=
     (N => 1,
      R => (I => 2));
begin
   Put_Line (Natural'Image (R.N + Natural (R.R.I)));
end Foo;
