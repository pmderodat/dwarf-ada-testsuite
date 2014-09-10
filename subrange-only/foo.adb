procedure Foo is

   function Saturate (V, L, U : Integer) return Integer is
      subtype Valid_Range is Integer range L .. U;
      Result : Valid_Range := V;
   begin
      return Result;
   end Saturate;

   procedure Nop (I : Integer) is
   begin
      null;
   end Nop;

begin
   Nop (Saturate (0, 1, 10));
   Nop (Saturate (1, 1, 10));
   Nop (Saturate (20, 1, 10));
end Foo;
