@echo off
call conda create -n paddle_cpu
call conda activate paddle_cpu
python -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
pip install "paddleocr>=2.0.1"
pip install -r requirements.txt
conda deactivate