files per automatizzare la slurm submission

il job che verra' eseguito e' 

./slurm_glidein_dcgp|booster.job

lo script di pressione e' 

slurm_queue_manager_dcgp|booster.py


Ricordarsi di creare: credential_leo_itb.idtoken  che NON deve essere in git


Nuove capability dynamic: slurm_queue_manager_dynamic.py  conf.json

legge conf.json a ogni iterazione, per cui si puo' modificare il comportamento mentre runna
per esempio, mettendo max_hours a 0 si ferma lo script


Le versioni  _lowprio.json sono usate per girare sulla qos=qos_lowprio, a bassa priorita' ma NON a pagamento 
