with Ada.Text_IO; use Ada.Text_IO;

procedure Foo is
   type Small is mod 2 ** 5;
   for Small'Size use 6;

   type PA_Type is array (Positive range <>) of Small;
   pragma Pack (PA_Type);

   A : PA_Type := (1, 2, 0, 0, 0, 6, 7, 8, 9, 10);
   B : PA_Type renames A (3 .. 5);
begin
   B := (3, 4, 5);
   Put_Line ("B (4) =" & Small'Image (B (4)));
end Foo;
