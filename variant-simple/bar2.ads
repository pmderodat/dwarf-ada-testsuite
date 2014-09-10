package Bar2 is
   type Arr_Type is array (Integer range <>) of Natural;
   function Get (I : Integer) return Arr_Type;
end Bar2;
