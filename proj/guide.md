# Steps to run horovod code on Power9


1.  Copy estimator_horovod folder from projects to your home. Change sam14XXX for your user
    ```
    cp -r /gpfs/projects/sam14/estimator_horovod /gpfs/home/sam14/sam14XXX/estimator_horovod/
    cd /gpfs/home/sam14/sam14XXX/estimator_horovod/
    ```
2.  In job_horovod.sh file, you have to:
    -   Set output and error directory. Change sam14XXX for your user
    -   Set nodes, tasks-per-node and gres gpu. gres gpu is GPUs per node. Task-per-node and gres gpu have to be same
    -   Set np flag of mpirun. This flag have to be nodes*tasks-per-node
    -   Set python's flags:
        -   train_dir and eval_dir are the data directory
        -   model_dir is directory where tensorflow will save checkpoint. You have to change it for each experiment
        -   We can try differents model_name like vgg_16, resnet_v2_50 or resnet_v2_101
3.  Now, you have to run job_horovod.sh file with:
    ```
    sbatch job_horovod.sh
    ```
4.  We could see the output in .err file, inside the jobs folder
        
        
    
