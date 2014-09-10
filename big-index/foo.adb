with Interfaces; use Interfaces;

procedure Foo is
   type Array_Type is array (Unsigned_64 range <>) of Integer;

   function Get (L, U : Unsigned_64) return Array_Type is
   begin
      return (L .. U => 12);
   end Get;

   A : constant Array_Type := Get(16#1_0000_0000#, 16#1_0000_000f#);

   procedure Discard (A : Array_Type) is
   begin
      null;
   end Discard;

begin
   Discard (A);
end Foo;
