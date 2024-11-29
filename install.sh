#!/bin/bash

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "请使用 root 权限运行此脚本"
    exit 1
fi

SERVICE_NAME="chatnio-blob-service"
CURRENT_DIR=$(pwd)
PORT=${1:-8000}  # 默认端口 8000，可通过参数修改

# 检查操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "无法确定操作系统类型"
    exit 1
fi

# 创建虚拟环境和安装依赖
echo "正在创建 Python 虚拟环境..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 创建启动脚本
echo "创建启动脚本..."
cat > start.sh << EOF
#!/bin/bash
cd $CURRENT_DIR
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port $PORT
EOF

chmod +x start.sh
SCRIPT="$CURRENT_DIR/start.sh"

# 创建系统服务
echo "创建系统服务..."
cat > /etc/systemd/system/"$SERVICE_NAME".service << EOF
[Unit]
Description=$SERVICE_NAME
After=network.target

[Service]
Type=simple
ExecStart=$SCRIPT
User=$SUDO_USER
Group=$SUDO_USER
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=$SERVICE_NAME

[Install]
WantedBy=multi-user.target
EOF

# 创建日志配置
if [ ! -f "/etc/rsyslog.d/$SERVICE_NAME.conf" ]; then
    echo "配置日志..."
    echo "if \$programname == '$SERVICE_NAME' then /var/log/$SERVICE_NAME.log" > /etc/rsyslog.d/$SERVICE_NAME.conf
    echo "& stop" >> /etc/rsyslog.d/$SERVICE_NAME.conf
    systemctl restart rsyslog
fi

# 创建存储目录
echo "创建存储目录..."
mkdir -p "$CURRENT_DIR/static"
chown -R $SUDO_USER:$SUDO_USER "$CURRENT_DIR/static"

echo "注册并启动服务..."
systemctl daemon-reload
systemctl start $SERVICE_NAME
systemctl enable $SERVICE_NAME

# 检查服务状态
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "服务已成功启动！"
    echo "服务状态："
    systemctl status $SERVICE_NAME
    echo -e "\n访问地址: http://localhost:$PORT"
    echo "日志文件: /var/log/$SERVICE_NAME.log"
else
    echo "服务启动失败，请检查日志："
    journalctl -u $SERVICE_NAME -n 50
    exit 1
fi
