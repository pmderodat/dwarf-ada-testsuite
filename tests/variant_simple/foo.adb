procedure Foo is
   type Rec_Type (I : Integer) is record
      B : Boolean;
      case I is
         when 0 =>
            null;
         when 1 .. 10 =>
            C : Character;
         when others =>
            N : Natural;
      end case;
   end record;

   procedure Nop (R : Rec_Type) is
   begin
      null;
   end Nop;

   R0 : constant Rec_Type := (I => 0, B => True);
   R2 : constant Rec_Type := (I => 2, B => True, C => 'A');
   R11 : constant Rec_Type := (I => 11, B => True, n => 11);

begin
   Nop (R0);
   Nop (R2);
   Nop (R11);
end Foo;
