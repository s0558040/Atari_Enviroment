# Tweaked enviroment for Atari Pong

## What does it do
Es handelt sich hierbei um einen Reinforcment Learning Algorythmus mit einem neuen Gym-Enviroment, welche seinen Reward anders vergibt, als es im Original der Fall war. Die Rewards sind: 10 für das Gewinnen einer Runde, -5 für das Verlieren einer Runde und 0 für alle anderen Zustände.

## How to use
Bevor Pong zum erstmal ausgeführt werden kann, müssen einige Pakete installiert werden (dies gilt für Ubuntu):
+ sudo apt install python-pip
+ pip install numpy
+ pip install gym
+ pip instal gym[atari]
+ Installation von Anaconda3 [Anaconda3-Download-Link](https://www.anaconda.com/distribution/)

Nach der Installation kann das Programm wie folgt gestartet werden:
+ chmod u+x pg-pong-ac.py
+ ./pg-pong-ac.py

oder

+ python pg-pong-ac.py

Für das erstellen eines Plottes wird Anaconda mit Jupyter-Notebook benötigt und wie folgt durchgeführt:
+ Wechseln in das Anaconda Verzeichnis
+ Starten des Jupyter-Notebooks: ./jupyter-notebook /pfad_zum_projektverzeichnis/
+ Ausführen des Codes der ersten Code-Zelle mithilfe des Play Buttons im Reiter
+ Plot wird sowohl im Jupyter-Notebook angezeigt, als auch in einer erzeugten PDF Datei gespeichert

Falls das Programm zum erstem mal gestartet wird muss in "pg-pong-ac.py" in der Zeile 19
`resume = True` zu `resume = False` geändert werden.
Für alle weiteren dürchläufe kann wieder True eingesetzt werden.

## Anmerkung
Die Plotts in der Dokumentation befinden sich zusaetzlich in separaten PDF Dateien in den Ordnern "Original_Reward" und "Veraenderter_Reward".

## Sources:
[Pong-Code](https://github.com/schinger/pong_actor-critic "Policy Gradient Code")

[Gym-Enviroment](https://github.com/openai/gym/tree/master/gym/envs)