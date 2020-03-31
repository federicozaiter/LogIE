# LogIE

### Requirements

Requirements are listed in `requirements.txt`. To install these, run:

```
pip install -r requirements.txt
```



#### OpenIE Methods Installation

For most methods, it requires to have Java installed additionally to Python as it runs third party tools.

##### Stanford

Install the Stanford CoreNLP from [here](https://stanfordnlp.github.io/CoreNLP/index.html#download). 

##### Ollie

Install Ollie using their "Local Machine" installation process you can find [here](https://github.com/knowitall/ollie#local-machine).

##### OpenIE5

Install OpenIE5 using their pre-compiled stand-alone JAR you can find [here](https://github.com/dair-iitd/OpenIE-standalone#using-pre-compiled-openie-standalone-jar).

Before using OpenIE5 you will need to run it as a server using a command similar to this one: ``java -Xmx10g -XX:+UseConcMarkSweepGC -jar openie-assembly-5.0-SNAPSHOT.jar --httpPort 8000 `` executing the downloaded stand-alone JAR. This is explained [here](https://github.com/dair-iitd/OpenIE-standalone#running-as-http-server) in their repo.

Additionally, it requires a python wrapper you can find [here](https://github.com/vaibhavad/python-wrapper-OpenIE5) which is already installed when you install the ``requirements.txt``.

##### PredPatt

Proceed to install PredPatt as they explain it in their repo [here](https://github.com/hltcoe/PredPatt/blob/master/doc/get-started.md#installation). 

##### ClausIE

Download ClauseIE from their source [here](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/software/clausie/).



#### Configuration File

After installing the OpenIE methods above, make sure to update the `openie.ini` configuration file located inside the `openie` package according to your installation. It provides part of the settings for running the OpenIE methods that depend on Java.



### Quick Start

#### Run LogIE

After the installation, run the following command in the home directory where this project is located.

`python -m LogIE.run --templates "<Templates File>" --evaluation he --rules team --openie stanford `

#### Arguments

```
python -m LogIE.run --help
usage: run.py [-h] [--templates templates] [--base_dir base_dir] [--templates_type templates_type] [--rules rules]
              [--evaluation evaluation [evaluation ...]] [--openie openie] [--id id]

Runs information extraction from logs.

optional arguments:
  -h, --help            show this help message and exit
  --templates templates
                        input raw templates file path (default: None)
  --base_dir base_dir   base output directory for output files (default: [<Project Folder>])
  --templates_type templates_type
                        Input type of templates. Choose from (['original', 'open_source'],). (default: ['original'])
  --rules rules         Predefined rules to extract triples from templates. (default: None)
  --evaluation evaluation [evaluation ...]
                        Triples extraction evaluation metrics. Choose from (['he', 'redundancy', 'counts'],).
                        (default: [])
  --openie openie       OpenIE approach to be used for triple extraction. Choose from ['stanford', 'openie5', 'ollie',
                        'predpatt', 'clausie']. (default: ['stanford'])
  --id id               Experiment id. Automatically generated if not specified. (default: None)
```

