#include <limits>
#include <vector>
#include <algorithm>

using namespace std;

float EED(const std::vector<int> hyp, const std::vector<int> ref, const float alpha, const float deletion,  const float insertion, const float rho){
    
    std::vector<int> lj(hyp.size() + 1, 0); //Coverage Tracker
    std::vector<float> row(hyp.size() + 1, 1); 
    row[0] = float(0); //EED initialisation 0,0 = 0 rest 1   
    std::vector<float> nextRow(hyp.size() + 1, std::numeric_limits<float>::max());
    
    int minInd; //Min index 
    int minimum; //Min value
    
    for(int w = 1; w < ref.size() + 1; ++w){
        
        for(int i = 0; i < hyp.size() + 1; ++i){ 
            if(i > 0){
             
              nextRow[i] = std::min({nextRow[i-1] + deletion, row[i-1] + (ref[w-1] != hyp[i-1]), row[i]+ insertion});        
            }
            else{
              nextRow[i] = row[i]+ 1.0;
            }
        }
      
        minimum = nextRow[0];
        minInd = 0;
        for(int i = 1; i < nextRow.size(); ++i){
           if(nextRow[i] < minimum){
              minInd = i;
              minimum = nextRow[minInd];
           }
        }
        lj[minInd] = lj[minInd] + 1;

        //Long Jumps 32 is the magic number for white spaces
        if(ref[w-1] == 32){
          float longJump = alpha + nextRow[minInd];
          for(int i = 0; i < nextRow.size(); ++i){
            if(nextRow[i] > longJump){
              nextRow[i] = longJump;
            }
          }
        } 
        row = nextRow;
        nextRow.assign(nextRow.size() ,std::numeric_limits<float>::max());
    }
    float coverage = 0;
    for(int i = 1; i < lj.size(); ++i){
      if(lj[i] > 1){
        coverage += lj[i];
      }
    } 
    float errors = row[row.size()-1];

    
    return (errors + rho*coverage)/(ref.size()+coverage);
}

//C wrapper for the C++ implementation. Communication channel with Python.
extern "C" float wrapper(const int* hyp, const int* ref, const int len_h, const int len_r,  const float alpha, const float deletion,  const float insertion, const float rho){
  std::vector<int> hyp_vec(hyp,hyp+len_h);
  std::vector<int> ref_vec(ref,ref+len_r);
  
  return EED(hyp_vec, ref_vec, alpha, deletion, insertion, rho);
}