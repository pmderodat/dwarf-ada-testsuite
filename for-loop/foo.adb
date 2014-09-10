with Ada.Containers.Vectors;
with Ada.Text_IO; use Ada.Text_IO;

procedure Foo is
   package Int_Vectors is new Ada.Containers.Vectors
     (Index_Type   => Positive,
      Element_Type => Integer);

   V : Int_Vectors.Vector;
begin
   for I_Val in 1 .. 5 loop
      V.Append (I_Val);
   end loop;

   for I of V loop
      Put_Line (Integer'Image (I));
   end loop;
end Foo;
