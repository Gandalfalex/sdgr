## TODOs ML:
[ ] Setting up ~~Flask~~ Django API
- change thesis in this regard, ORM is important point
- ~~upload~~ and get to view TestData
- define ML Components, build hiarchy to connect them
- readFromDB to get projects, some form of navigation and accessing would be nice?
- find a way to start training models
- integrate models

[ ] Setup small python kafka consumer that creates numpy files

[x] integrate REACT frontend for djangoAPI

[ ] think about using same server/different app for both ML and TSD

[ ] find a way to integrate GPUs with model (TODO from Home, not office)
- [tf gpu](https://wandb.ai/authors/ayusht/reports/Using-GPUs-With-Keras-A-Tutorial-With-Code--VmlldzoxNjEyNjE)
- use callbacks to track time and others, might work with Graylog... get this working
- threading to run each training in separate thread... not the main thread.

[ ] change to use numpy array and convert it to String

[ ] comparing signals to stop training without running out of iterations




## Whats finished:

[x] DataSet are now PlainData, everything else inherits from PlainData

[x] small kafka consumer in python to create numpy arrays ready for upload

[x] Update UI to adapt to the new data structure

[x] Upload of numpy files and viewing them is done! Backend




## Open to debate:
Save model to DB as binary 

pros:
- ACID
- no dead links, ...

cons:
-  performance?
-  its easier to save as file, but do we need ftp server later?





docker build -t gandalfalex/custom-sus:latest .


## TODO

Anforderugnsanalyse (aus Personas)

Infrastruckturkrieterien
