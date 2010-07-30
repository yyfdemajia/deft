// -*- mode: C++; -*-

/*
 * counted_ptr - simple reference counted pointer.
 *
 * The is a non-intrusive implementation that allocates an additional
 * int and pointer for every counted object.
 */

#pragma once

struct counter {
  counter(void* p = 0, unsigned c = 1) : ptr(p), count(c) {}
  void* ptr;
  unsigned count;
};

template <class X> class counted_ptr {
public:
  explicit counted_ptr(X* p = 0) // allocate a new counter
    : itsCounter(0) {
    if (p) itsCounter = new counter(p);
  }
  ~counted_ptr() { release(); }
  counted_ptr(const counted_ptr& r) {
    acquire(r.itsCounter);
  }
  counted_ptr& operator=(const counted_ptr& r) {
    if (this != &r) {
      release();
      acquire(r.itsCounter);
    }
    return *this;
  }

  //template <class Y> friend class counted_ptr<Y>;
  template <class Y> counted_ptr(const counted_ptr<Y>& r) {
    acquire(r.itsCounter);
  }
  template <class Y> counted_ptr& operator=(const counted_ptr<Y>& r) {
    if (this != &r) {
      release();
      acquire(r.itsCounter);
    }
    return *this;
  }

  // A const counted_ptr means we can't modify what it points to!
  const X &operator*() const { return *(X *)itsCounter->ptr; }
  const X *operator->() const { return (X *)itsCounter->ptr; }

  X &operator*() { return *(X *)itsCounter->ptr; }
  X *operator->() { return (X *)itsCounter->ptr; }
  bool unique() const {
    return (itsCounter ? itsCounter->count == 1 : true);
  }

  // The rest should all be private, but I don't understand out to do
  // the friend class thing above.  :(

  counter *itsCounter;
  //private:
  void acquire(counter* c) {
    // increment the count
    itsCounter = c;
    if (c) ++c->count;
  }
  void release() {
    // decrement the count, delete if it is 0
    if (itsCounter) {
      if (--itsCounter->count == 0) {
        delete (X *)itsCounter->ptr;
        delete itsCounter;
      }
      itsCounter = 0;
    }
  }
};
