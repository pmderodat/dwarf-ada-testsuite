package Pck is
   type Record_Type (Length : Natural) is record
      S : String (1.. Length);
   end record;
end Pck;
