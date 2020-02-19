executable = ../ncrfpp_run.sh 
getenv = True
output = data/logs/swb_train.out
error = data/logs/swb_train.err
log = data/logs/swb_train.log
requirements = (CUDACapability >= 1.2) && $(requirements:True)
request_GPUs = 2 
transfer_executable = False
arguments = "swb1/swb.train.config"
notification = complete
queue
