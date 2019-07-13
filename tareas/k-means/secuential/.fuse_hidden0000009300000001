#include <chrono>
#include <string>
#include <tuple>
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <random>
using namespace std;

using Point = vector<double>;

using DataFrame = vector<Point>;

void print(const Point& p) {
  for( size_t i = 0; i < p.size(); i++) {
    cout << " " << p[i];
  }
  cout << endl;
}

inline double sdistance(const Point& first, const Point& second) {
  double d = 0.0;
  for(size_t dim = 0; dim < first.size(); dim++) {
    d += (first[dim] - second[dim])*(first[dim] - second[dim]);
  }
  return d;
}

void printStats(size_t k, const vector<size_t>& assignments, const DataFrame& c) {
  vector<size_t> counts(k,0);
  for (const size_t& i : assignments) {
    counts[i]++;
  }

  for(size_t i = 0; i < k; i++) {
    cout << "c[" << i << "] has " << counts[i] << " points" << endl;
    print(c[i]);
  }
}


DataFrame readData(string filename) {
  DataFrame data;
  ifstream input(filename);
  string line;
  while (getline(input, line)) {
    istringstream iss(line);
    double x, y, z, w;
    string a;
    iss >> x >> y >> z >> w >> a;
    Point p;
    p.push_back(x);
    p.push_back(y);
    p.push_back(z);
    p.push_back(w);
    //cout << x << p[0] << endl;
    data.push_back(p);
  }
  cout << data.size() << endl;
  return data;
}

pair<DataFrame,vector<size_t>> kmeans(const DataFrame& data, size_t k) {//const DataFrame& cluster
  size_t iterations = 1000;
  size_t dimensions = data[0].size();
  static random_device seed;
  static mt19937 random_gen(seed());
  uniform_int_distribution<size_t> indices(0, data.size()-1);

  DataFrame means(k);
  
  for(Point& cluster : means) {
    size_t i = indices(random_gen);
    cluster = data[i];
    // cout << "Selected point at position " << i << endl;
    //print(cluster);
  }


  vector<size_t> assignments(data.size());
  for (size_t it = 0; it < iterations; it++) {
    // Find assignments
    for (size_t point = 0; point < data.size(); point++) {
      double best_distance = numeric_limits<double>::max();
      size_t best_cluster = 0;
      for(size_t cluster = 0; cluster < k; cluster++) {
        double distance = sdistance(data[point], means[cluster]);
        if(distance < best_distance) {
          best_distance = distance;
          best_cluster = cluster;
        }
      }
      assignments[point] = best_cluster;
    }
    //printStats(k,assignments);
    //cout << endl;
    DataFrame newmeans(k,vector<double>(dimensions,0.0));

    vector<size_t> counts(k, 0);
    for(size_t point = 0; point < data.size(); point++) {
      size_t cluster = assignments[point];
      for(size_t d = 0; d < dimensions; d++) {
        newmeans[cluster][d] += data[point][d];
      }
      counts[cluster] += 1;
    }

    for(size_t cluster = 0; cluster < k; cluster++) {
      size_t count = max<size_t>(1, counts[cluster]);
      for(size_t d = 0; d < dimensions; d++) {
        means[cluster][d] = newmeans[cluster][d] / count;
      }
    }
  }
  return {means, assignments};
}

int main(int argc, const char* argv[]) {
  cout << "Kmeans!!!" << endl;
  if (argc < 4) {
    cerr << "excecute: kmeans.cpp <data-file> dim <k> [runs] <data-cluster>"
              << endl;
    exit(EXIT_FAILURE);
  }
  DataFrame data = readData(argv[1]);
  const auto dim = atoi(argv[2]);
  auto k = atoi(argv[3]);
  const unsigned int number_of_runs = (argc <= 15) ? atoi(argv[4]) : 15;
  DataFrame centroides = readData(argv[5]);
  
  DataFrame c;
  vector<size_t> a;

  double total_elapsed = 0;
  for (int run = 0; run < number_of_runs; ++run) {
    const auto start = chrono::high_resolution_clock::now();
  	tie(c,a) = kmeans(data, k);
    const auto end = chrono::high_resolution_clock::now();
    const auto duration =
        chrono::duration_cast<chrono::duration<double>>(end - start);
    total_elapsed += duration.count();
  }
  cerr << "Took: " << total_elapsed / number_of_runs << "s (" << number_of_runs << " runs)" << endl;

  printStats(k, a, c);
  return 0;
}
