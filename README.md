files per automatizzare la slurm submission

il job che verra' eseguito e' 

./slurm_glidein_dcgp|booster.job

lo script di pressione e' 

slurm_queue_manager_dcgp|booster.py


Ricordarsi di creare: credential_leo_itb.idtoken  che NON deve essere in git


Nuove capability dynamic: slurm_queue_manager_dcgp_dynamic.py

legge dcgp.json a ogni iterazione, per cui si puo' modificare il comportamento mentre runna

