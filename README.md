# Forum_website
Assessment and Feedback mode: 运行assessment_backend.py 运行服务端
Recommendation mode: 运行recommendation.py运行服务端

在forum文件夹下运行live-server

下次启动程序时需要的步骤（Recommendation mode）：
运行 bin/elasticsearch.bat 启动数据库服务器
在BERT model 文件夹   F:\CodesForPapers\data_and_model\uncased_L-12_H-768_A-12
运行 
C:\Users\Penguin\AppData\Roaming\Python\Python36\Scripts\bert-serving-start.exe -model_dir uncased_L-12_H-768_A-12\ -num_worker=1 -max_seq_len=128
打开BERT server
