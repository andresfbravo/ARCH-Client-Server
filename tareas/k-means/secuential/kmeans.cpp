//#include <algorithm>
#include <cassert>
#include <chrono>
//#include <cstdlib>
#include <fstream>
#include <iostream>
//#include <limits>
#include <random>
#include <sstream>
#include <vector>
#include <math.h>

using namespace std;
/*
struct Point {
  double x{0}, y{0};
};*/
/*
struct Point {
  vector<double> p;
};*/

//vector<vector<double>>;
using Point = vector<double>;
using DataFrame = vector<Point>;

/*
double squared_l2_distance(vector<double> &f, vector<double> &s){
  double suma = 0;
  cout<<"distancia"<<endl;
  
  for(int i = 0; i<f.size();++i){
    suma += (f[i] - s[i])*(f[i] - s[i]);
  }
  
  cout<<"termina distancia"<<endl;
  return sqrt(suma);
}*/

/*
double squared_l2_distance(Point first, Point second) {

	return sqrt(((first.x - second.x)*(first.x - second.x)) + ((first.y - second.y)*(first.y - second.y)));
}*/

DataFrame k_means(const DataFrame& data, unsigned k, unsigned number_of_iterations, const DataFrame& cluster) {//, const DataFrame& centroides


  static random_device seed;
  static mt19937 random_number_generator(seed());
  uniform_int_distribution<unsigned> indices(0, data.size() - 1);

  // Pick centroids as random points from the dataset.
  DataFrame means(k);
  /* Genere cluster with aleatory points */
  for (auto& cluster : means) {
    cluster = data[indices(random_number_generator)];
  }


  double suma = 0;
  vector<unsigned int> assignments(data.size());
  for (unsigned int iteration = 0; iteration < number_of_iterations; ++iteration) {
    // Find assignments.
    for (unsigned int point = 0; point < data.size(); ++point) {
      double best_distance = numeric_limits<double>::max();
      unsigned int best_cluster = 0;
      for (unsigned int cluster = 0; cluster < k; ++cluster) {
          for(int i = 0; i<data[0].size();++i){
            //suma += (data[point][i] - means[cluster][i])*(data[point][i] - means[cluster][i]);
            //cout<<"i="<<i<<endl;
          }
            const double distance = suma;
//          const double distance = squared_l2_distance(& data[point],& means[cluster]);
        if (distance < best_distance) {
          best_distance = distance;
          best_cluster = cluster;
        }
      }
      assignments[point] = best_cluster;
    }
 	//cout<<"they are the cluster: "<<cluster<<endl;



    //cout<<"Sum up and count points for each cluster."<<endl;
    // Sum up and count points for each cluster.
    DataFrame new_means(k,vector<double>(3,0.0));
    vector<unsigned int> counts(k, 0);
    for (unsigned int point = 0; point < data.size(); ++point) {
      const unsigned int cluster = assignments[point];
      //recorro el vector con las dimensiones
      for(int i=0 ; i<k;++i){
        new_means[cluster][i] += data[point][i];
      }      
      counts[cluster] += 1;

      //new_means[cluster].x += data[point].x;
      //new_means[cluster].y += data[point].y;
    }
    //cout<<"Divide sums by counts to get new centroids."<<endl;
    // Divide sums by counts to get new centroids.
    for (unsigned int cluster = 0; cluster < k; ++cluster) {
      // Turn 0/0 into 0/1 to avoid zero division.
      const unsigned int count = max<size_t>(1, counts[cluster]);
      //recorro el vector
      //cout<<means[0].size()endl;
      for(int i=0 ; i<k;++i){

        means[cluster][i] = new_means[cluster][i]/count;
        cout<<"i: "<<i<<endl;
      }

      //means[cluster].x = new_means[cluster].x / count;
      //means[cluster].y = new_means[cluster].y / count;
    }

  }

  return means;
}

int main(int argc, const char* argv[]) {
  cout<<"welcome"<<endl;
  if (argc < 4) {
    cerr << "excecute: kmeans.cpp <data-file> dim <k> [runs] <data-cluster>"
              << endl;
    exit(EXIT_FAILURE);
  }
  cout<<"welcome2"<<endl;
  const auto dim = atoi(argv[2]);
  cout<<"welcome3"<<endl;
  const auto k = atoi(argv[3]);
  cout<<"welcome4"<<endl;
  //const auto iterations = (argc >= 4) ? atoi(argv[3]) : 300;
  unsigned int iterations = 1000;
  const unsigned int number_of_runs = (argc <= 15) ? atoi(argv[4]) : 15;
  cout<<"welcome5"<<endl;

  cout<<"inicia lectura"<<endl;
 
  vector<double> punto;
  DataFrame data;
  ifstream stream(argv[1]);
  if (!stream) {
    cerr << "Could not open file: " << argv[1] << endl;
    exit(EXIT_FAILURE);
  }
  string line;
  double x;
  while (getline(stream, line)) {
    //Point point;
    istringstream line_stream(line);
   // size_t label;
    for(int i=0;i<dim;i++){
      line_stream >> x;//point.x >> point.y >> label;
      punto.push_back(x);
    }

    data.push_back(punto);
  }
  cout<<data.size()<<endl;


  cout<<"termina lectura de datos"<<endl;
//leo argumentos los centroides iniciales
  cout<<"inicia lectura centroides iniciales"<<endl;

  vector<double> punto2;
  DataFrame centroides;
  ifstream stream2(argv[5]);
  if (!stream2) {
    cerr << "Could not open file: " << argv[5] << endl;
    exit(EXIT_FAILURE);
  }
  string line2;
  double q;
  while (getline(stream2, line2)) {
    //Point point;
    istringstream line_stream(line2);
    size_t label;
    for(int i=0;i<dim;++i){
      line_stream >>q;//point.x >> point.y >> label;
      punto2.push_back(q);
    }

    centroides.push_back(punto2);
  }
  cout<<centroides.size()<<endl;


  cout<<"termina lectura centroides iniciales"<<endl;




  DataFrame means(k);
  double total_elapsed = 0;
  for (int run = 0; run < number_of_runs; ++run) {
    const auto start = chrono::high_resolution_clock::now();
    means = k_means(data, k, iterations,centroides);
    const auto end = chrono::high_resolution_clock::now();
    const auto duration =
        chrono::duration_cast<chrono::duration<double>>(end - start);
    total_elapsed += duration.count();
  }
  cerr << "Took: " << total_elapsed / number_of_runs << "s ("
            << number_of_runs << " runs)" << endl;
  cout<<"tamaño de means: "<<means.size()<<endl;
  //cout<<means<<endl;
  for (int i=0;i<means.size();i++) {
    for(int j=0;j<dim;j++){
      cout << means[i][j] << " " <<endl;
    }
    //cout << mean.x << " " << mean.y << endl;
  }
  cout<<"\n";
  
}