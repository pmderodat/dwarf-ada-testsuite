package body Foo is

   Length : Natural := 200;

   type Record_Type;
   type Record_Access is access all Record_Type;
   type Record_Type is record
      Value : String (1 .. Length + 1);
      Next  : Record_Access;
   end record;

   function Foobar (R : Record_Access) return Record_Access;

   function Bar return Natural is
      R : Record_Access := new Record_Type'((others => ' '), null);
      N : Natural := 0;
   begin
      Length := 1;
      while R /= null loop
         N := N + 1;
         R := Foobar (R.Next);
      end loop;
      return N;
   end Bar;

   function Foobar (R : Record_Access) return Record_Access is
   begin
      return R.Next;
   end Foobar;

end Foo;
