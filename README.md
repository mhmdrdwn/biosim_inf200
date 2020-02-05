# Simulation of Ecosystem in Rossumøya

The project used test-driven approach for modeling of the ecosystem in the island Rossumøya. Rossumøya is an imaginary island that has different landscapes "Desert, Savannah, Jungle, Ocean, Mountain". Landscapes have different animals types 'Hebivores, Carnivores'. Herbivores are meat eater and Carnivores are veggy eater. The animals eats based on their fitness (animals with higher fitness eat first). The life cycle of the simulation starts with feeding all animals in cells. Second stage is procreation where animals give birth. Animals give birth based on their probability of giving birth and based on the number of the animals in the cell. Third stage is migration where animals migrate based on the order of their fitnesses and based on the individual probability of animals to migrate. Animals migrate only from current cell to adjacent diagonal cells. Forth stage is animals growing up where their fitnesses and weights decrease. last stage is dying stage where animals with higher probability fto die will be removed from the cells. 

Further details about the project is given in:
[exam_sheet](https://github.com/mhmdrdwn/BioSim_G26_Mohamed_Nasibeh/blob/master/exam_sheet.pdf)

Project design:
```
src/biosim/
```

Simulation Results:
```
results/
```

Presentation:
```
Exam/
```

To run the simulation:
```
python Examples/check_sim.py
```
