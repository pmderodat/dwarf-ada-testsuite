package Pkg is
   type Rec_Type (C : Character := 'd') is record
      case C is
         when Character'First     => X_First : Integer;
         when Character'Val (127) => X_127   : Integer;
         when Character'Val (128) => X_128   : Integer;
         when Character'Last      => X_Last  : Integer;
         when others              => null;
      end case;
   end record;
   R : Rec_Type;
end Pkg;
