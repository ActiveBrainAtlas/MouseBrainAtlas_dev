# Information for the User

*  __[Atlas Scripts](../demo/README.md)__: A set of scripts that encapsulate the pipeline of the Atlas project. The user must simply enter the listed commands step by step.

 0. Training Classifier  [not ready]
 1. Preprocessing [being tested]
 2. Detection
 3. Registration
 4. Visualization
 5. Atlas Building
 
<br/><br/>

# Information for the Developer

## In Depth Atlas Scripts
Here is documentation of [Atlas Scripts in-depth](running_scripts/README.md) which includes all input files, output files, and input arguments for every script.


## Server Information
Information having to do with the BirdStore and S3 servers this project uses. S3 is the primary location of all data and interfacing with it may be necessary. BirdStore, as of right now, is synced with S3 but is not used directly for file retrieval.
- [AWS Instructions](writeup/AWS_instruction.md)
  - Guide for transferring files to/from AWS S3 and Birdstore as well as running code on AWS with CfnCluster

## Atlas Project Information
These files contain information on what software is needed to run the code, how all of the processed data is organized both locally and on relevant servers, and a catalog of every brain that has gone through the code.
- [Software Dependancies](dependancies.md)
  - List of all packages that need to be installed 
- [Stack Directories](Brain_stack_directories.md)
  - Description of every stack, all relevant information]

## Documentation Files
 Following are all of the documentation files and user guides for the Atlas code. Having had multiple developers working on it, there are documentation files deemed "historical" that were made by earlier developers. Certain documents are also marked as incomplete and should be ignored by non-developers. Several "historical" files are unmarked as they are not outdated.
