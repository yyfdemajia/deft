#include <stdio.h>
#include <time.h>
#include <cassert>
#include <math.h>
#include <stdlib.h>
#include <popt.h>
#include <sys/stat.h>
#include <string.h>
#include <errno.h>
#include "handymath.h"
#include "vector3d.h"

#include "version-identifier.h"

// ---------------------------------------------------------------------
// Define "Constants" -- set from arguments then unchanged
// ---------------------------------------------------------------------

double M = 0;      // Define our initial system magnetization.
double J = 1;      // Define our spin coupling.
double minT = 0.2; // Define minimum Temperature.

const int Q = 2;   // Define number of spin states.

// ---------------------------------------------------------------------
// ising.h files -- this could likely go into an ising.h file
// ---------------------------------------------------------------------

struct ising_simulation {
  long iteration;   // the current iteration number
  int N;            // N*N is the number of sites
  int *S;
  double E;      // system energy.
  double T;      // canonical temperature.

  long energy_levels;
  long *energy_histogram;

  explicit ising_simulation(int N); // generate the spin lattice

  int random_flip(int oldspin) const; // pick a new random (but changed) spin

  void reset_histograms();
  void flip_a_spin();
  double calculate_energy();
};

// ising_simulation methods

void ising_simulation::reset_histograms(){

  for(int i = 0; i < energy_levels; i++){
    energy_histogram[i] = 0;
  }
}

int ising_simulation::random_flip(int oldspin) const {
  if (Q==2) return -oldspin;

  return random::ran64() % Q - Q/2; // gives value -Q/2 to Q/2-1?
}

ising_simulation::ising_simulation(int NN) {
  iteration = 0;
  E = 0;
  T = 0;
  N = NN;
  S = new int[N*N];
  // Energy histogram
  // abs. ground state energy for 2D Ising model.  But with new long rather
  // than just long for energy_histogram could I keep track of energy levels
  // found and update as needed?
  // i.e. if H(E) == 0 then energy_levels ++ "we have found a new energy".
  energy_levels = 2*J*N*N;
  energy_histogram = new long[energy_levels]();
  //printf("energy_levels %ld\n", energy_levels);
  reset_histograms();

  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      S[i+N*j] = 1; // initialize to all 1s
    }
  }
}

void ising_simulation::flip_a_spin() {
  iteration += 1;
  int k = random::ran64() % (N*N);
  int i = k % N;
  int j = k / N;
  int old = S[j + i*N];
  S[j + i*N] = random_flip(S[j + i*N]);

  int neighbor_spins = S[j + ((i+1) % N)*N] + S[j + ((i-1+N) % N)*N] +
                       S[((j+1) % N) + i*N] + S[((j-1+N) % N) + i*N];

// ---------------------------------------------------------------------
// Canonical Monte-Carlo
// ---------------------------------------------------------------------

  const double deltaE = J*(old - S[j + i*N])*neighbor_spins;
  const double lnprob = -deltaE/T;

  if (lnprob < 0 && random::ran() > exp(lnprob)) {
    S[j + i*N] = old;
    //printf("not flipping from E=%g\n", E);
  } else {
    E += deltaE;
    //printf("flipping gives E=%g\n", E);
  }

  energy_histogram[abs(lround(E))] += 1;
// ---------------------------------------------------------------------
// Broad-Histogram Methods
// ---------------------------------------------------------------------
}

double ising_simulation::calculate_energy() {
  E = 0;
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      // we want to enforce periodic boundary conditions.
      int neighbor_spins = S[(i+1) % N + j*N] + S[i + ((j+1) % N)*N];

      E += -J*neighbor_spins*S[i+j*N];
    }
  }
  return E;
}

// ---------------------------------------------------------------------
// Initialize Main
// ---------------------------------------------------------------------

static double took(const char *name) {
  assert(name); // so it'll count as being used...
  static clock_t last_time = clock();
  clock_t t = clock();
  double seconds = (t-last_time)/double(CLOCKS_PER_SEC);
  if (seconds > 120) {
    printf("%s took %.0f minutes and %g seconds.\n", name, seconds/60,
           fmod(seconds,60));
  } else {
    printf("%s took %g seconds...\n", name, seconds);
  }
  fflush(stdout);
  last_time = t;
  // We round our times to a close power of e to make our code more
  // likely to be reproducible, i.e. so two runs with identical
  // parameters (including random number seed) should (unless we are
  // unlucky) result in identical output.
  return exp(ceil(log(seconds)));
}

int main(int argc, const char *argv[]) {

  ising_simulation ising(4);
  ising.T = 2;

  took("Starting program");
  printf("version: %s\n",version_identifier());

  long totaliteration = 12000;

  ising.calculate_energy();
  for (long i = 0; i < totaliteration; i++) {
    ising.flip_a_spin();
  }
  printf("I think the energy is %g\n", ising.E);
  ising.calculate_energy();
  printf("the energy is %g\n", ising.E);
  
  took("Running");
  for(int i = 0; i <= ising.energy_levels; i++){
    printf("energy histogram at %d is %ld\n",i,ising.energy_histogram[i]);
  }
  // -------------------------------------------------------------------
  // END OF MAIN PROGRAM LOOP
  // -------------------------------------------------------------------

  delete[] ising.energy_histogram;

}

