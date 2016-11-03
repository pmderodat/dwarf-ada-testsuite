class A
{
public:
  int a;
  int b;

  void foo () {};
};

class B : public A
{
};

int main()
{
  B b;
  b.foo ();
  return 0;
}
