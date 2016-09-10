package Foo is
   type Rec_Type (I : Integer := 0) is record
      case I is
         when 0 =>
            I0 : Integer;
         when 1 .. 0 =>
            I1 : Integer;
         when 1 .. 10 | Integer'Last .. Integer'First =>
            I2 : Integer;
         when others => null;
      end case;
   end record;
   R : Rec_Type;
end Foo;
