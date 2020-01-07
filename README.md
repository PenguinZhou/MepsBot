# MepsBot in the simulated online mental health community
Assessment-based mode: run **assessment_backend.py** to start the backend server
Recommendation-based mode: run **recommendation.py** to start the backend server

Start the live-server under the **Forum** directory to run the community website locally. For example, open the Forum directory using Visual Studio Code, and run the command **live-server** in its terminal. 

下次启动程序时需要的步骤（Recommendation mode）：
运行 bin/elasticsearch.bat 启动数据库服务器
在BERT model 文件夹   F:\CodesForPapers\data_and_model\uncased_L-12_H-768_A-12
运行 
C:\Users\Penguin\AppData\Roaming\Python\Python36\Scripts\bert-serving-start.exe -model_dir uncased_L-12_H-768_A-12\ -num_worker=1 -max_seq_len=128
打开BERT server
