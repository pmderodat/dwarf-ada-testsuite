procedure Simple is
   type Rec_Type (I : Integer := 0) is record
      case I is
         when 0 =>
            null;
         when 1 .. 10 =>
            C : Character;
         when others =>
            N : Natural;
      end case;
   end record;
   pragma Unchecked_Union (Rec_Type);

   function Get (I : Integer) return Rec_Type is
   begin
     case I is
        when 0       => return (I => 0);
        when 1 .. 10 => return (I => 1, C => 'A');
        when others  => return (I => 11, N => abs I);
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
end Simple;
