executable = ../ncrfpp_run.sh 
getenv = True
requirements = (CUDACapability >= 1.2) && $(requirements:True)
request_GPUs = 2
transfer_executable = False
notification = complete

output = data/logs/swb_decode.$(Process).out
error = data/logs/swb_decode.$(Process).err
log = data/logs/swb_decode.$(Process).log

arguments = "swb1/ptb.decode.config"
queue

arguments = "swb1/ms.decode.config"
queue
