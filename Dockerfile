# 使用Python作为基础镜像  
FROM python:3.10-slim-buster  
  
# 设置工作目录  
WORKDIR /app  
  
COPY requirements.txt requirements.txt
# 安装Flask和其他Python依赖项  
RUN pip install --upgrade pip
RUN pip install --upgrade gevent
RUN pip install --no-cache-dir -r requirements.txt
  
# 复制Flask应用代码到容器中  
COPY . .  
  
# 如果你的Go代码需要构建，这里添加构建步骤  
# 例如：RUN go build -o mygoapp .  
  
# 设置环境变量  
ENV FLASK_APP=app.py  
ENV FLASK_RUN_HOST=0.0.0.0  
ENV FLASK_RUN_PORT=3002 
  
# 暴露端口  
EXPOSE 3001  
  
# 定义容器启动时运行的命令  
ENTRYPOINT [ "gunicorn", "-c", "gunicorn.conf", "demo2:app" ]
#CMD [ "--app", "/app/app.py", "run", "--host=0.0.0.0","--port=5000" ]
