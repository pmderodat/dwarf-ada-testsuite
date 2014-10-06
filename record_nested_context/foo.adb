procedure Foo is
   type Foo_Type is record
      I : Integer;
   end record;

   function Get_I (F : Foo_Type) return Integer is
   begin
      return F.I;
   end Get_I;

   procedure Discard (I : Integer) is
   begin
      null;
   end Discard;

   F : Foo_Type := (I => 2);

begin
   Discard (Get_I (F));
end Foo;
