# 使用 AWS Lambda Python 3.9 官方基础镜像
FROM public.ecr.aws/lambda/python:3.9

# 设置工作目录
WORKDIR ${LAMBDA_TASK_ROOT}

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制 Lambda 函数代码
COPY lambda_function.py .

# 设置 Lambda 函数入口点
CMD ["lambda_function.lambda_handler"]

