package Foo is
   function Foo (I : Integer) return Integer is (2 * I);

   subtype Small_Type is Integer range Foo (0) .. Foo (5);
   type Data_Type (I : Small_Type := 0) is record
      S : String (1 .. I);
   end record;
   type Array_Type is array (Integer range <>) of Data_Type;

   No_Data : constant Data_Type;
   procedure Discard (D : Data_Type);
   procedure Discard (A : Array_Type);

private
   No_Data : constant Data_Type := Data_Type'(I => 0, S => <>);
end Foo;
