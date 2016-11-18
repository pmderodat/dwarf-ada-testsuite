package Pkg is
   subtype Lower_Range is Character range
      Character'Val (0) .. Character'Val (127);
   subtype Middle_Range is Character range
      Character'Val (64) .. Character'Val (164);
   subtype Upper_Range is Character range
      Character'Val (128) .. Character'Val (255);

   LR : Lower_Range;
   MR : Middle_Range;
   UR : Upper_Range;
end Pkg;
