struct foo {
  int i;
};

typedef struct foo bar;

void foobar(void)
{
  struct foo f = {1};
  bar b;

  b.i = f.i + 1;
}
