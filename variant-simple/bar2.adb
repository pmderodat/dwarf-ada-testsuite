package body Bar2 is
   function Get (I : Integer) return Arr_Type is
     ((0 .. I => 0));
end Bar2;
