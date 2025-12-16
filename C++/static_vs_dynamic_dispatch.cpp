#include <iostream>
using namespace std;

// Base class
class Cat {
public:
  void speakStatic() { cout << "Im a static dispatched cat object" << endl; }

  virtual void speakDynamic() {
    cout << "Im a dynamically dispatched cat object" << endl;
  }
};

// Derived class
class Binx : public Cat {
public:
  void speakStatic() {
    cout << "Im Joe's statically dispatched cat named Binx" << endl;
  }

  void speakDynamic() override {
    cout << "Im Joe's dynamically dispatched cat named Binx" << endl;
  }
};

int main() {
  // Creating objects of base and derived classes
  Cat cat_obj;
  Binx binx_obj;
  ;

  // Base class pointer pointing to derived class object
  Cat *ptr = &binx_obj;

  cout << "Calling non-virtual function through base pointer:" << endl;
  ptr->speakStatic();

  cout << "Calling virtual function through base pointer:" << endl;
  ptr->speakDynamic();

  return 0;
}