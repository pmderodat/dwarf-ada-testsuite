package body Procs is

   function Proc1 (R : Record_Type) return Natural is
   begin
      return R.S'Length;
   end Proc1;

   function Proc2 (R : Record_Type) return Natural is
   begin
      return R.S'Last;
   end Proc2;

end Procs;
