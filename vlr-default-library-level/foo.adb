package body Foo is
   procedure Discard (D : Data_Type) is
      type Array_Type is array (Integer range <>) of Data_Type;
      A : Array_Type := (1 => D);
   begin
      null;
   end Discard;

   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;
end Foo;
