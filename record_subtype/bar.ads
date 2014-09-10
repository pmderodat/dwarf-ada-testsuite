package Bar is
   type R1_T (B : Boolean) is null record;
   subtype R2_T is R1_T;
   subtype R3_T is R1_T (B => False);
   subtype R4_T is R3_T;

   type R5_T is record
      A : R1_T (B => True);
      B : R1_T (B => False);
   end record;

   subtype R6_T is R5_T;
   type R7_T is new R5_T;


   R1 : R1_T := (B => False);
   R2 : R2_T := (B => True);
   R3 : R3_T;
   R4 : R4_T;
   R5 : R5_T;
   R6 : R6_T;
   R7 : R7_T;
end Bar;
