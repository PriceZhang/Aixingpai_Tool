@echo off  
call conda activate paddle_cpu
python main.py  
conda deactivate