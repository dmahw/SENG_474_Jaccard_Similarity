SENG 474 Programming Assignment Locality Sensitivity and Jaccard Similarity
===========================================================================

## Developers
* David Mah
* Adam Leung

## Description
This respository contains 2 solutions, jaccard similarity, and jaccard similarity with locality sensitivity. Both computes similarities between a database of questions. With locality sensitivity hashing, we can compute similarities in larger datasets much quicker. 

This repository has been reposted to hide sensitive information.

## Requirements
Ensure the following python packages/libraries are available on your system (some packages should already by made available in python):
* Python 3
* fnv (This is included with fnv.py)
* numpy
* sys
* uuid
* datetime
* re

## Instructions
1. Run the respective commands below for each part

Part 1 Jaccard Similarity:
1. Ensure question_[*].tsv is in the same directory as jaccardSimilarity.py
2. Run `python jaccardSimilarity.py question_[*].tsv`
3. The program will terminate once it has been completed. The output file will be named question_sim_[*].tsv
* For submission, the output question_sim_4k.tsv has been provided
* question_150k.tsv is extremely large and expensive to run using jaccardSimilarity

Part 2 Jaccard Similarity with Locality Sensitive Hashing Algorithm:
1. Ensure question_[*].tsv is in the same directory as localSensitivity.py
2. Run `python localSensitivity.py question_[*].tsv`
3. The program will terminate once it has been completed denoted by the '... completed minhashing with local sensitivity hashing' message. During the execution, a few status messages with a time will be printed to the console.
4. The output file will be named question_sim_[*].tsv
* For submission, the output question_sim_150k.tsv has been provided 
