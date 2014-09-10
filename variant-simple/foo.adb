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

   function Get (I : Integer) return Rec_Type is
   begin
     case I is
        when 0       => return (I => 0, B => True);
        when 1 .. 10 => return R : Rec_Type (I) do
                           R.B := True;
                           R.C := 'A';
                        end return;
        when others  => return (I => 12, B => True,  N => abs I);
     end case;
   end Get;

   procedure Nop (R : Rec_Type) is
   begin
      null;
   end Nop;

   R0 : constant Rec_Type := Get (0);
   R1 : constant Rec_Type := Get (1);
   R11 : constant Rec_Type := Get (11);

begin
   Nop (R0);
   Nop (R1);
   Nop (R11);
end Foo;
