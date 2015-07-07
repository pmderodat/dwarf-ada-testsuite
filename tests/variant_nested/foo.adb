procedure Foo is
   type Rec_Type (I1, I2 : Integer) is record
      B : Boolean;
      S1 : String (1 .. I1);
      case I1 is
         when 0 =>
            null;
         when 1 .. 10 =>
            S2 : String (1 .. I2);
            case I2 is
               when 0 =>
                  null;
               when 2 .. 20 | 22 =>
                  C : Character;
               when others =>
                  N2 : Natural;
            end case;
         when others =>
            N1 : Natural;
      end case;
   end record;

   function Get (I : Integer) return Rec_Type is
   begin
     case I is
        when 0 =>
           return (I1 => 0,
                   I2 => 0,
                   B  => True,
                   S1 => (others => 'A'));
        when 1 .. 10 => return R : Rec_Type (I, 2) do
                           R.B := True;
                           R.S2 := (others => 'B');
                           R.C := 'C';
                        end return;
        when others =>
           return (I1 => 12,
                   I2 => 0,
                   B  => True,
                   S1 => (others => 'B'),
                   N1 => abs I);
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
