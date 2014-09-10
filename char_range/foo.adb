with Ada.Text_IO; use Ada.Text_IO;

procedure Foo is
   type Array_Type is array (Character range <>) of Natural;
   subtype Array_Type1 is Array_Type (Character);
   subtype Array_Type2 is Array_Type (Character range 'a' .. 'z');

   A1 : Array_Type1 := (others => 0);
   A2 : Array_Type2 := (others => 0);
begin
   A1 ('a') := 1;
   A1 ('b') := 2;
   A2 := A1 ('a' .. 'z');
   A1 ('c') := A2 ('a') + A2 ('b');
end Foo;
