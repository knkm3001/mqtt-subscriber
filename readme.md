# MQTT Subscriber

k8sにデプロイする前に以下対応を行って開発及びテストする。

ホスト側で以下実行
```
>> k port-forward --address 0.0.0.0 svc/my-mysql-cluster 3306:3306
```

`.env`ファイルを修正。内容は以下。
- MQTT_BROKER_IP: mqttブローカーが動作しているk8sのLoadbaLancerのIP
- MQTT_BROKER_PORT: mqttブローカーが動作しているk8sのLoadbaLancerのport番号
- MQTT_TOPIC: `sensor/#` でOK
- MYSQL_USER: user name
- MYSQL_ROOT_PASSWORD: user password
- MYSQL_HOST_NAME: `host.docker.internal:3306` でOK。port-fowardを通してk8s上のmysqlへアクセスできるようにする
- MYSQL_DB_NAME: `sensor` でOK

以下実行し、コンテナへアクセス
```
>> docker build -t core.harbor.ing.k8s-cluster.internal/sensor-data/mqtt-subscribe:latest . 
>> docker run --rm  --env-file .env -d core.harbor.ing.k8s-cluster.internal/sensor-data/mqtt-subscribe:latest
>> docker exec -it <container id> /bin/bash
```

DBのテーブルを修正する必要あれば以下実行
```
/app# python models.py 
create tables start
fin
```


問題なさそうならpush
```
>> docker push core.harbor.ing.k8s-cluster.internal/sensor-data/mqtt-subscribe:latest
```