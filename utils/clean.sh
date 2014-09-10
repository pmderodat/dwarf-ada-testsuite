#! /bin/sh

for pattern in "b~*" foo "*.o" "*.ali" "*.s" "*.gnatdt" "*.gnatG"
do
    find . -name "$pattern" -delete
done

find . -type f -executable -not -name "*.sh" -delete
